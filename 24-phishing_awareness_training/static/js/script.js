document.addEventListener('DOMContentLoaded', function() {
    const quizForm = document.getElementById('quiz-form');
    
    if (quizForm) {
        quizForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitQuiz();
        });
    }
});

function submitQuiz() {
    const formData = new FormData(document.getElementById('quiz-form'));
    const answers = {};
    
    // Collect all answers
    document.querySelectorAll('input[type="radio"]:checked').forEach(input => {
        const questionId = input.name.replace('question_', '');
        answers[questionId] = parseInt(input.value);
    });
    
    // Send to server
    fetch('/submit_quiz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answers: answers })
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error submitting quiz. Please try again.');
    });
}

function displayResults(data) {
    const quizContainer = document.getElementById('quiz-container');
    const resultsContainer = document.getElementById('results-container');
    
    quizContainer.style.display = 'none';
    resultsContainer.style.display = 'block';
    
    let resultsHTML = `
        <div class="card">
            <div class="card-header bg-${data.percentage >= 80 ? 'success' : 'warning'} text-white">
                <h3>Quiz Results</h3>
            </div>
            <div class="card-body">
                <div class="text-center mb-4">
                    <h4>Score: ${data.score}/${data.total} (${data.percentage.toFixed(1)}%)</h4>
                    <div class="progress">
                        <div class="progress-bar bg-${data.percentage >= 80 ? 'success' : 'warning'}" 
                             style="width: ${data.percentage}%"></div>
                    </div>
                </div>
    `;
    
    if (data.percentage >= 80) {
        resultsHTML += `
            <div class="alert alert-success text-center">
                <h5>Congratulations! You passed!</h5>
                <a href="/certificate" class="btn btn-success mt-2">
                    <i class="fas fa-award"></i> Get Your Certificate
                </a>
            </div>
        `;
    } else {
        resultsHTML += `
            <div class="alert alert-warning text-center">
                <h5>Keep learning! Try again to improve your score.</h5>
                <button onclick="location.reload()" class="btn btn-warning mt-2">
                    <i class="fas fa-redo"></i> Retry Quiz
                </button>
            </div>
        `;
    }
    
    resultsHTML += `<h5>Detailed Results:</h5>`;
    
    data.results.forEach(result => {
        const question = document.querySelector(`[data-question-id="${result.question_id}"]`);
        const questionText = question ? question.querySelector('.question-text').textContent : 'Question';
        
        resultsHTML += `
            <div class="card mb-3 ${result.is_correct ? 'border-success' : 'border-danger'}">
                <div class="card-body">
                    <h6>${questionText}</h6>
                    <p class="${result.is_correct ? 'text-success' : 'text-danger'}">
                        <strong>Your answer:</strong> ${getOptionText(result.question_id, result.user_answer)}
                        ${result.is_correct ? '✓' : '✗'}
                    </p>
                    ${!result.is_correct ? `
                        <p class="text-success">
                            <strong>Correct answer:</strong> ${getOptionText(result.question_id, result.correct_answer)}
                        </p>
                    ` : ''}
                    <p class="text-muted"><strong>Explanation:</strong> ${result.explanation}</p>
                </div>
            </div>
        `;
    });
    
    resultsHTML += `</div></div>`;
    resultsContainer.innerHTML = resultsHTML;
}

function getOptionText(questionId, optionIndex) {
    const questionElement = document.querySelector(`[data-question-id="${questionId}"]`);
    if (questionElement) {
        const optionLabel = questionElement.querySelector(`input[value="${optionIndex}"] + label`);
        return optionLabel ? optionLabel.textContent : 'Unknown option';
    }
    return 'Unknown option';
}