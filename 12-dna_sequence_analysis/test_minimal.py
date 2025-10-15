from Bio import SeqIO
from Bio.SeqUtils import ProtParam

def test_minimal():
    """Minimal test to check basic functionality"""
    print("=== MINIMAL FUNCTIONALITY TEST ===\n")
    
    # Test sequence download and basic parsing
    try:
        # Read the downloaded sequence
        record = SeqIO.read("data/sequences/P01308.fasta", "fasta")
        print(f"✓ Sequence parsed successfully: {record.id}")
        print(f"✓ Description: {record.description}")
        print(f"✓ Sequence length: {len(record.seq)} amino acids")
        print(f"✓ First 50 residues: {str(record.seq)[:50]}")
        
        # Test protein analysis
        protein_analyzer = ProtParam.ProteinAnalysis(str(record.seq))
        print(f"✓ Protein analysis successful")
        print(f"✓ Isoelectric point: {protein_analyzer.isoelectric_point():.2f}")
        print(f"✓ Instability index: {protein_analyzer.instability_index():.2f}")
        
        print("\n✓ ALL BASIC TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_minimal()