from src.sequence_downloader import SequenceDownloader
from src.sequence_analyzer import SequenceAnalyzer
import os

def test_basic_functionality():
    """Test basic functionality without BLAST"""
    print("=== TESTING BASIC FUNCTIONALITY ===\n")
    
    downloader = SequenceDownloader()
    analyzer = SequenceAnalyzer()
    
    try:
        # Download sequence
        uniprot_id = "P01308"  # Human Insulin
        print(f"Downloading sequence: {uniprot_id}")
        sequence_file = downloader.download_from_uniprot(uniprot_id)
        
        # Analyze sequence
        print("Analyzing sequence...")
        sequence_analysis = analyzer.analyze_protein_sequence(sequence_file)
        
        # Display results
        stats = analyzer.generate_sequence_stats(sequence_analysis)
        print(stats)
        
        print("Basic functionality test PASSED!")
        return True
        
    except Exception as e:
        print(f"Test FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    test_basic_functionality()