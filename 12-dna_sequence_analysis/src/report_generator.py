from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np  # Add this import
import os
from config.settings import RESULTS_DIR

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        os.makedirs(RESULTS_DIR, exist_ok=True)
    
    def generate_analysis_report(self, sequence_analysis, blast_results, output_file):
        """Generate comprehensive PDF report"""
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        
        story.append(Paragraph("DNA/PROTEIN SEQUENCE ANALYSIS REPORT", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Sequence Information
        story.append(Paragraph("1. SEQUENCE INFORMATION", self.styles['Heading2']))
        seq_info = [
            ["Sequence ID:", sequence_analysis['sequence_id']],
            ["Description:", sequence_analysis['sequence_description']],
            ["Length:", f"{sequence_analysis['sequence_length']} amino acids"],
            ["Molecular Weight:", f"{sequence_analysis['molecular_weight']:.2f} Da"],
            ["Isoelectric Point:", f"{sequence_analysis['isoelectric_point']:.2f}"],
            ["Instability Index:", f"{sequence_analysis['instability_index']:.2f}"],
            ["GRAVY:", f"{sequence_analysis['gravy']:.3f}"]
        ]
        
        seq_table = Table(seq_info, colWidths=[2*inch, 4*inch])
        seq_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(seq_table)
        story.append(Spacer(1, 0.2*inch))
        
        # BLAST Results Summary
        story.append(Paragraph("2. BLAST ANALYSIS RESULTS", self.styles['Heading2']))
        
        if blast_results:
            top_hits = blast_results[:5]  # Show top 5 hits
            
            blast_data = [["Hit ID", "Description", "E-value", "Bit Score", "% Identity"]]
            for hit in top_hits:
                blast_data.append([
                    hit['sequence_id'][:20],
                    hit['sequence_def'][:30] + "..." if len(hit['sequence_def']) > 30 else hit['sequence_def'],
                    f"{hit['e_value']:.2e}",
                    f"{hit['bit_score']:.1f}",
                    f"{hit['percent_identity']:.1f}%"
                ])
            
            blast_table = Table(blast_data, colWidths=[1.2*inch, 2*inch, 1*inch, 1*inch, 1*inch])
            blast_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(blast_table)
        else:
            story.append(Paragraph("No significant BLAST hits found.", self.styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Generate and add plots
        self.generate_plots(sequence_analysis, blast_results, story)
        
        # Build PDF
        doc.build(story)
        print(f"Report generated: {output_file}")
    
    def generate_plots(self, sequence_analysis, blast_results, story):
        """Generate analysis plots and add to report"""
        try:
            # Amino Acid Composition Plot
            plt.figure(figsize=(10, 6))
            aa_data = sequence_analysis['amino_acid_composition']
            plt.bar(aa_data.keys(), [x * 100 for x in aa_data.values()])
            plt.title('Amino Acid Composition')
            plt.xlabel('Amino Acids')
            plt.ylabel('Percentage (%)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            plot_path = os.path.join(RESULTS_DIR, 'aa_composition.png')
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            # Add plot to report
            story.append(Paragraph("3. AMINO ACID COMPOSITION", self.styles['Heading2']))
            story.append(Image(plot_path, width=6*inch, height=4*inch))
            story.append(Spacer(1, 0.2*inch))
            
            # BLAST Results Visualization
            if blast_results:
                plt.figure(figsize=(10, 6))
                df = pd.DataFrame(blast_results[:10])  # Top 10 hits
                
                # Handle very small e-values
                e_values = df['e_value'].copy()
                e_values[e_values == 0] = 1e-300  # Replace 0 with very small number
                
                plt.scatter(df['percent_identity'], -np.log10(e_values))
                plt.xlabel('Percentage Identity (%)')
                plt.ylabel('-log10(E-value)')
                plt.title('BLAST Hits: Identity vs E-value')
                plt.tight_layout()
                
                blast_plot_path = os.path.join(RESULTS_DIR, 'blast_analysis.png')
                plt.savefig(blast_plot_path, dpi=300, bbox_inches='tight')
                plt.close()
                
                # Add BLAST plot to report
                story.append(Paragraph("4. BLAST ANALYSIS VISUALIZATION", self.styles['Heading2']))
                story.append(Image(blast_plot_path, width=6*inch, height=4*inch))
                
        except Exception as e:
            print(f"Warning: Could not generate plots: {str(e)}")
            story.append(Paragraph("Note: Visualization generation failed due to technical issues.", self.styles['Normal']))