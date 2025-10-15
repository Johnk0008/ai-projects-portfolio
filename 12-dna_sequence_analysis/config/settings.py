# NCBI and UniProt API settings
NCBI_BLAST_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
UNIPROT_API_URL = "https://rest.uniprot.org/uniprotkb/"
ENTREZ_EMAIL = "Johnykumar0008@gmail.com"  # Required for NCBI API

# File paths
SEQUENCE_DIR = "data/sequences"
RESULTS_DIR = "data/results"

# BLAST parameters
BLAST_PARAMS = {
    'program': 'blastp',
    'database': 'swissprot',
    'expect': 10,
    'gapopen': 11,
    'gapextend': 1,
    'matrix': 'BLOSUM62'
}