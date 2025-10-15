import os
import sys
from src.sequence_downloader import SequenceDownloader
from src.sequence_analyzer import SequenceAnalyzer
from src.blast_analyzer import BlastAnalyzer
from src.report_generator import ReportGenerator
from config.settings import RESULTS_DIR

def main():
    print("=== DNA/PROTEIN SEQUENCE ANALYSIS TOOL ===\n")
    
    # Initialize components
    downloader = SequenceDownloader()
    analyzer = SequenceAnalyzer()
    blast_analyzer = BlastAnalyzer()
    report_gen = ReportGenerator()
    
    try:
        # Example: Download Insulin protein from UniProt
        uniprot_id = "P01308"  # Human Insulin
        print(f"Downloading sequence: {uniprot_id}")
        
        # Download sequence
        sequence_file = downloader.download_from_uniprot(uniprot_id)
        
        # Analyze sequence
        print("Analyzing sequence...")
        sequence_analysis = analyzer.analyze_protein_sequence(sequence_file)
        
        # Display sequence statistics
        stats = analyzer.generate_sequence_stats(sequence_analysis)
        print(stats)
        
        # Ask user if they want to perform BLAST (since it can be slow)
        response = input("\nPerform BLAST analysis? This may take 5-15 minutes. (y/n): ")
        
        blast_results = []
        if response.lower() in ['y', 'yes']:
            # Perform BLAST analysis
            print("Starting BLAST analysis...")
            blast_file = blast_analyzer.perform_blastp(sequence_file)
            
            # Parse BLAST results
            print("Parsing BLAST results...")
            blast_results = blast_analyzer.parse_blast_results(blast_file)
            top_hits = blast_analyzer.get_top_hits(blast_results, 10)
            
            # Display top BLAST hits
            print("\nTOP BLAST HITS:")
            print("=" * 100)
            print(f"{'Hit ID':<20} {'Description':<40} {'E-value':<12} {'Bit Score':<10} {'% Identity':<10}")
            print("-" * 100)
            for hit in top_hits:
                print(f"{hit['sequence_id'][:20]:<20} {hit['sequence_def'][:40]:<40} "
                      f"{hit['e_value']:<12.2e} {hit['bit_score']:<10.1f} {hit['percent_identity']:<10.1f}")
        else:
            print("Skipping BLAST analysis.")
        
        # Generate comprehensive report
        report_file = os.path.join(RESULTS_DIR, f"analysis_report_{uniprot_id}.pdf")
        report_gen.generate_analysis_report(sequence_analysis, blast_results, report_file)
        
        print(f"\nAnalysis complete! Report saved: {report_file}")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()