import numpy as np
import pandas as pd
from Bio.Seq import Seq
from Bio import SeqUtils
import random

class SequenceProcessor:
    def __init__(self):
        self.amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
        self.nucleotides = 'ACGT'
    
    def generate_sample_data(self, n_samples=1000):
        """Generate sample protein sequences and labels"""
        sequences = []
        labels = []
        
        for i in range(n_samples):
            if i < n_samples // 2:
                # Generate enzyme-like sequences
                seq = self._generate_enzyme_sequence()
                label = 'Enzyme'
            else:
                # Generate non-enzyme sequences
                seq = self._generate_non_enzyme_sequence()
                label = 'Non-Enzyme'
            
            sequences.append(seq)
            labels.append(label)
        
        return sequences, labels
    
    def _generate_enzyme_sequence(self):
        """Generate enzyme-like sequences with specific patterns"""
        length = random.randint(50, 200)
        # Enzymes often have specific motifs
        motifs = ['GxGxxG', 'DxSxG', 'GxSxG']
        motif = random.choice(motifs)
        
        seq = ''
        for char in motif:
            if char == 'x':
                seq += random.choice(self.amino_acids)
            else:
                seq += char
        
        # Add random sequence
        remaining_length = length - len(seq)
        if remaining_length > 0:
            seq += ''.join(random.choices(self.amino_acids, k=remaining_length))
        
        return seq
    
    def _generate_non_enzyme_sequence(self):
        """Generate random protein sequences"""
        length = random.randint(50, 200)
        return ''.join(random.choices(self.amino_acids, k=length))
    
    def extract_sequence_features(self, sequences):
        """Extract various features from protein sequences"""
        features = []
        
        for seq in sequences:
            feature_dict = {
                'sequence_length': len(seq),
                'molecular_weight': self._calculate_molecular_weight(seq),
                'aromaticity': self._calculate_aromaticity(seq),
                'instability_index': self._calculate_instability_index(seq),
                'isoelectric_point': self._calculate_isoelectric_point(seq),
                'hydrophobicity': self._calculate_hydrophobicity(seq),
                'charge': self._calculate_charge(seq)
            }
            
            # Amino acid composition
            for aa in self.amino_acids:
                feature_dict[f'freq_{aa}'] = seq.count(aa) / len(seq)
            
            # Secondary structure propensity
            feature_dict.update(self._secondary_structure_features(seq))
            
            features.append(feature_dict)
        
        return features
    
    def _calculate_molecular_weight(self, seq):
        """Calculate approximate molecular weight"""
        # Simplified calculation
        aa_weights = {'A': 89, 'C': 121, 'D': 133, 'E': 147, 'F': 165,
                     'G': 75, 'H': 155, 'I': 131, 'K': 146, 'L': 131,
                     'M': 149, 'N': 132, 'P': 115, 'Q': 146, 'R': 174,
                     'S': 105, 'T': 119, 'V': 117, 'W': 204, 'Y': 181}
        return sum(aa_weights.get(aa, 0) for aa in seq)
    
    def _calculate_aromaticity(self, seq):
        """Calculate aromaticity score"""
        aromatic_aas = ['F', 'W', 'Y']
        aromatic_count = sum(1 for aa in seq if aa in aromatic_aas)
        return aromatic_count / len(seq)
    
    def _calculate_instability_index(self, seq):
        """Calculate instability index"""
        # Simplified version
        dipeptide_instability = {
            'GD': 1, 'AP': 1, 'PG': 1, 'GS': 1  # Example values
        }
        instability = 0
        for i in range(len(seq) - 1):
            dipeptide = seq[i:i+2]
            instability += dipeptide_instability.get(dipeptide, 0)
        return instability / (len(seq) - 1) if len(seq) > 1 else 0
    
    def _calculate_isoelectric_point(self, seq):
        """Calculate approximate isoelectric point"""
        # Simplified calculation
        acidic_aas = ['D', 'E']
        basic_aas = ['K', 'R', 'H']
        acidic_count = sum(1 for aa in seq if aa in acidic_aas)
        basic_count = sum(1 for aa in seq if aa in basic_aas)
        return (acidic_count - basic_count) / len(seq) + 6.0  # Approximate
    
    def _calculate_hydrophobicity(self, seq):
        """Calculate hydrophobicity index"""
        hydrophobic_aas = ['A', 'V', 'L', 'I', 'P', 'F', 'W', 'M']
        hydrophobic_count = sum(1 for aa in seq if aa in hydrophobic_aas)
        return hydrophobic_count / len(seq)
    
    def _calculate_charge(self, seq):
        """Calculate net charge at pH 7"""
        positive_aas = ['K', 'R', 'H']  # Basic amino acids
        negative_aas = ['D', 'E']       # Acidic amino acids
        positive_charge = sum(1 for aa in seq if aa in positive_aas)
        negative_charge = sum(1 for aa in seq if aa in negative_aas)
        return positive_charge - negative_charge
    
    def _secondary_structure_features(self, seq):
        """Calculate secondary structure propensity"""
        # Chou-Fasman parameters (simplified)
        helix_formers = ['E', 'A', 'L', 'M', 'Q', 'K', 'R', 'H']
        sheet_formers = ['V', 'I', 'Y', 'F', 'W', 'T', 'C']
        
        helix_propensity = sum(1 for aa in seq if aa in helix_formers) / len(seq)
        sheet_propensity = sum(1 for aa in seq if aa in sheet_formers) / len(seq)
        coil_propensity = 1 - (helix_propensity + sheet_propensity)
        
        return {
            'helix_propensity': helix_propensity,
            'sheet_propensity': sheet_propensity,
            'coil_propensity': coil_propensity
        }