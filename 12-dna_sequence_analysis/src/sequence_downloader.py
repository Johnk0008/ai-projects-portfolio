import requests
from Bio import Entrez
from Bio import SeqIO
import os
from config.settings import SEQUENCE_DIR, ENTREZ_EMAIL

class SequenceDownloader:
    def __init__(self):
        Entrez.email = ENTREZ_EMAIL
        os.makedirs(SEQUENCE_DIR, exist_ok=True)
    
    def download_from_uniprot(self, uniprot_id):
        """Download protein sequence from UniProt"""
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
        response = requests.get(url)
        
        if response.status_code == 200:
            file_path = os.path.join(SEQUENCE_DIR, f"{uniprot_id}.fasta")
            with open(file_path, 'w') as f:
                f.write(response.text)
            print(f"Sequence downloaded: {file_path}")
            return file_path
        else:
            raise Exception(f"Failed to download sequence: {response.status_code}")
    
    def download_from_ncbi(self, accession_id, db="protein"):
        """Download sequence from NCBI"""
        try:
            handle = Entrez.efetch(db=db, id=accession_id, rettype="fasta", retmode="text")
            sequence_data = handle.read()
            handle.close()
            
            file_path = os.path.join(SEQUENCE_DIR, f"{accession_id}.fasta")
            with open(file_path, 'w') as f:
                f.write(sequence_data)
            print(f"Sequence downloaded: {file_path}")
            return file_path
        except Exception as e:
            raise Exception(f"Error downloading from NCBI: {str(e)}")
    
    def read_sequence(self, file_path):
        """Read sequence from FASTA file"""
        with open(file_path, 'r') as f:
            return f.read()