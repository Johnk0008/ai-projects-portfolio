from Bio.SeqUtils import ProtParam
from Bio.SeqUtils import molecular_weight
from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd

class SequenceAnalyzer:
    def __init__(self):
        pass
    
    def analyze_protein_sequence(self, sequence_file):
        """Perform comprehensive protein sequence analysis"""
        record = SeqIO.read(sequence_file, "fasta")
        sequence = str(record.seq)
        
        # Protein analysis
        protein_analyzer = ProtParam.ProteinAnalysis(sequence)
        
        # Calculate molecular weight - FIXED version
        # For proteins, we need to use the protein molecular weight calculation
        mol_weight = self.calculate_protein_mw(sequence)
        
        analysis_results = {
            'sequence_id': record.id,
            'sequence_description': record.description,
            'sequence_length': len(sequence),
            'molecular_weight': mol_weight,
            'amino_acid_composition': protein_analyzer.get_amino_acids_percent(),
            'aromaticity': protein_analyzer.aromaticity(),
            'instability_index': protein_analyzer.instability_index(),
            'isoelectric_point': protein_analyzer.isoelectric_point(),
            'secondary_structure_fraction': protein_analyzer.secondary_structure_fraction(),
            'molar_extinction_coefficient': protein_analyzer.molar_extinction_coefficient(),
            'gravy': protein_analyzer.gravy()  # Grand average of hydropathicity
        }
        
        return analysis_results
    
    def calculate_protein_mw(self, sequence):
        """Calculate molecular weight for protein sequence"""
        # Amino acid molecular weights (monoisotopic)
        aa_weights = {
            'A': 89.0935, 'R': 174.2017, 'N': 132.1184, 'D': 133.1032,
            'C': 121.1590, 'Q': 146.1451, 'E': 147.1299, 'G': 75.0669,
            'H': 155.1552, 'I': 131.1736, 'L': 131.1736, 'K': 146.1882,
            'M': 149.2124, 'F': 165.1900, 'P': 115.1310, 'S': 105.0930,
            'T': 119.1197, 'W': 204.2262, 'Y': 181.1894, 'V': 117.1469
        }
        
        # Calculate total weight minus water molecules (n-1 for peptide chain)
        total_weight = sum(aa_weights.get(aa, 0) for aa in sequence)
        # Subtract water molecular weight for each peptide bond
        water_loss = 18.0153 * (len(sequence) - 1)
        
        return total_weight - water_loss
    
    def generate_sequence_stats(self, analysis_results):
        """Generate formatted statistics from analysis"""
        stats = f"""
        SEQUENCE ANALYSIS REPORT
        ========================
        Sequence ID: {analysis_results['sequence_id']}
        Description: {analysis_results['sequence_description']}
        Length: {analysis_results['sequence_length']} amino acids
        Molecular Weight: {analysis_results['molecular_weight']:.2f} Da
        Isoelectric Point (pI): {analysis_results['isoelectric_point']:.2f}
        Instability Index: {analysis_results['instability_index']:.2f}
        Aromaticity: {analysis_results['aromaticity']:.3f}
        GRAVY: {analysis_results['gravy']:.3f}
        
        AMINO ACID COMPOSITION:
        """
        
        for aa, percentage in analysis_results['amino_acid_composition'].items():
            stats += f"        {aa}: {percentage*100:.2f}%\n"
        
        return stats