// Global variables
let currentChart = 'income-statement';

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadKeyMetrics();
    loadChart('income-statement');
    loadBalanceSheet();
    loadExpenseBreakdown();
    
    // Set up tab click events
    document.querySelectorAll('.nav-link[data-chart]').forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const chartType = this.getAttribute('data-chart');
            loadChart(chartType);
            
            // Update active tab
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
});

// Load key financial metrics
async function loadKeyMetrics() {
    try {
        const response = await fetch('/api/financial-summary');
        const data = await response.json();
        
        const metricsContainer = document.getElementById('key-metrics');
        metricsContainer.innerHTML = '';
        
        const metrics = [
            {
                title: 'Revenue',
                value: formatCurrency(data.revenue.current),
                change: data.revenue.growth,
                icon: 'fa-dollar-sign',
                color: 'primary'
            },
            {
                title: 'Net Income',
                value: formatCurrency(data.net_income.current),
                change: data.net_income.growth,
                icon: 'fa-chart-line',
                color: data.net_income.current >= 0 ? 'success' : 'danger'
            },
            {
                title: 'Gross Margin',
                value: data.gross_margin.current.toFixed(1) + '%',
                change: data.gross_margin.change,
                icon: 'fa-percentage',
                color: 'info'
            },
            {
                title: 'Current Ratio',
                value: data.current_ratio.current.toFixed(2),
                change: data.current_ratio.change,
                icon: 'fa-balance-scale',
                color: data.current_ratio.current >= 1.5 ? 'success' : 
                       data.current_ratio.current >= 1 ? 'warning' : 'danger'
            }
        ];
        
        metrics.forEach(metric => {
            const changeClass = metric.change > 0 ? 'positive' : 
                              metric.change < 0 ? 'negative' : 'neutral';
            const changeIcon = metric.change > 0 ? 'fa-arrow-up' : 
                             metric.change < 0 ? 'fa-arrow-down' : 'fa-minus';
            const changeText = metric.change !== 0 ? Math.abs(metric.change).toFixed(1) + '%' : 'No change';
            
            const metricHtml = `
                <div class="col-lg-3 col-md-6 col-12 mb-3">
                    <div class="card metric-card border-${metric.color}">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="card-subtitle mb-2 text-muted">${metric.title}</h6>
                                    <h4 class="metric-value text-${metric.color}">${metric.value}</h4>
                                </div>
                                <div class="text-${metric.color}">
                                    <i class="fas ${metric.icon} fa-2x"></i>
                                </div>
                            </div>
                            <div class="metric-change ${changeClass}">
                                <i class="fas ${changeIcon} me-1"></i>
                                ${changeText}
                            </div>
                        </div>
                    </div>
                </div>
            `;
            metricsContainer.innerHTML += metricHtml;
        });
        
    } catch (error) {
        console.error('Error loading metrics:', error);
    }
}

// Load main chart based on type
async function loadChart(chartType) {
    currentChart = chartType;
    const chartElement = document.getElementById('main-chart');
    
    try {
        chartElement.classList.add('loading');
        
        let endpoint;
        switch(chartType) {
            case 'income-statement':
                endpoint = '/api/income-statement';
                break;
            case 'profitability':
                endpoint = '/api/profitability-metrics';
                break;
            case 'cash-flow':
                endpoint = '/api/cash-flow';
                break;
            case 'forecast':
                endpoint = '/api/forecast';
                break;
            default:
                endpoint = '/api/income-statement';
        }
        
        const response = await fetch(endpoint);
        const data = await response.json();
        
        if (data.chart || data.forecast_chart) {
            const chartData = JSON.parse(data.forecast_chart || data.chart);
            Plotly.newPlot('main-chart', chartData.data, chartData.layout);
        }
        
    } catch (error) {
        console.error('Error loading chart:', error);
        chartElement.innerHTML = '<div class="alert alert-danger">Error loading chart data</div>';
    } finally {
        chartElement.classList.remove('loading');
    }
}

// Load balance sheet data
async function loadBalanceSheet() {
    try {
        const response = await fetch('/api/balance-sheet');
        const data = await response.json();
        
        // Create assets pie chart
        const assetsTrace = {
            values: Object.values(data.assets),
            labels: Object.keys(data.assets),
            type: 'pie',
            name: 'Assets',
            domain: { row: 0, column: 0 }
        };
        
        const liabilitiesTrace = {
            values: Object.values(data.liabilities_equity),
            labels: Object.keys(data.liabilities_equity),
            type: 'pie',
            name: 'Liabilities & Equity',
            domain: { row: 0, column: 1 }
        };
        
        const pieLayout = {
            grid: { rows: 1, columns: 2 },
            title: 'Balance Sheet Composition',
            height: 200
        };
        
        Plotly.newPlot('balance-sheet-chart', [assetsTrace, liabilitiesTrace], pieLayout);
        
        // Display liquidity ratios
        const ratiosHtml = `
            <div class="row text-center">
                <div class="col-6">
                    <h6>Current Ratio</h6>
                    <h4 class="${data.current_ratio >= 1.5 ? 'text-success' : 
                               data.current_ratio >= 1 ? 'text-warning' : 'text-danger'}">
                        ${data.current_ratio.toFixed(2)}
                    </h4>
                </div>
                <div class="col-6">
                    <h6>Quick Ratio</h6>
                    <h4 class="${data.quick_ratio >= 1 ? 'text-success' : 
                               data.quick_ratio >= 0.5 ? 'text-warning' : 'text-danger'}">
                        ${data.quick_ratio.toFixed(2)}
                    </h4>
                </div>
            </div>
        `;
        document.getElementById('liquidity-ratios').innerHTML = ratiosHtml;
        
    } catch (error) {
        console.error('Error loading balance sheet:', error);
    }
}

// Load expense breakdown
async function loadExpenseBreakdown() {
    try {
        const response = await fetch('/api/trends');
        const data = await response.json();
        
        const chartData = JSON.parse(data.expense_breakdown_chart);
        Plotly.newPlot('expense-breakdown-chart', chartData.data, chartData.layout);
        
    } catch (error) {
        console.error('Error loading expense breakdown:', error);
    }
}

// Utility function to format currency
function formatCurrency(amount) {
    if (Math.abs(amount) >= 1000000) {
        return '$' + (amount / 1000000).toFixed(1) + 'M';
    } else if (Math.abs(amount) >= 1000) {
        return '$' + (amount / 1000).toFixed(1) + 'K';
    } else {
        return '$' + Math.round(amount).toLocaleString();
    }
}

// Auto-refresh data every 5 minutes
setInterval(() => {
    loadKeyMetrics();
    loadChart(currentChart);
}, 300000);