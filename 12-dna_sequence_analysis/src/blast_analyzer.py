from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO
import os
import time
from config.settings import RESULTS_DIR, ENTREZ_EMAIL

class BlastAnalyzer:
    def __init__(self):
        os.makedirs(RESULTS_DIR, exist_ok=True)
    
    def perform_blastp(self, sequence_file, evalue=0.001, hits=50):
        """Perform BLASTP analysis on protein sequence"""
        print("Performing BLASTP analysis... This may take several minutes.")
        
        # Read sequence
        record = SeqIO.read(sequence_file, "fasta")
        
        # Perform BLAST
        result_handle = NCBIWWW.qblast(
            program="blastp",
            database="swissprot",
            sequence=record.seq,
            expect=evalue,
            hitlist_size=hits,
            format_type="XML"
        )
        
        # Save results
        blast_file = os.path.join(RESULTS_DIR, f"blast_results_{record.id}.xml")
        with open(blast_file, "w") as out_handle:
            out_handle.write(result_handle.read())
        
        result_handle.close()
        
        print(f"BLAST results saved: {blast_file}")
        return blast_file
    
    def parse_blast_results(self, blast_file):
        """Parse BLAST XML results and extract relevant information"""
        with open(blast_file) as result_handle:
            blast_records = NCBIXML.parse(result_handle)
            
            results = []
            for blast_record in blast_records:
                for alignment in blast_record.alignments:
                    for hsp in alignment.hsps:
                        result = {
                            'sequence_id': alignment.hit_id,
                            'sequence_def': alignment.hit_def,
                            'length': alignment.length,
                            'e_value': hsp.expect,
                            'bit_score': hsp.bits,
                            'identity': hsp.identities,
                            'alignment_length': hsp.align_length,
                            'query_start': hsp.query_start,
                            'query_end': hsp.query_end,
                            'subject_start': hsp.sbjct_start,
                            'subject_end': hsp.sbjct_end,
                            'alignment': hsp.query + "\n" + hsp.match + "\n" + hsp.sbjct
                        }
                        # Calculate percentage identity and similarity
                        result['percent_identity'] = (hsp.identities / hsp.align_length) * 100
                        result['percent_similarity'] = self.calculate_similarity(hsp)
                        results.append(result)
            
            return results
    
    def calculate_similarity(self, hsp):
        """Calculate similarity percentage from HSP"""
        # This is a simplified calculation - in practice, you might use substitution matrices
        matches = sum(1 for a, b in zip(hsp.query, hsp.sbjct) if a == b or 
                     (a != '-' and b != '-' and a != ' ' and b != ' '))
        return (matches / hsp.align_length) * 100
    
    def get_top_hits(self, results, top_n=10):
        """Get top N hits sorted by bit score"""
        return sorted(results, key=lambda x: x['bit_score'], reverse=True)[:top_n]