"""Script to extract data from DisProt and create two files: 

1. Recoded DisProt fasta file
2. corresponding UniProt fasta file

Author: jcapecci09
"""

import subprocess
import os

def parse_consensus(fasta: str, recoded_fasta: str) -> list[str]:
    """Parses consensus IDR data from DisProt. Consensus sequences have the
    following format.

    >disprot|DP00004|full acc=P49913
    --------------------------------------------------------------------------------
    -----------------------------------------------------TTTTTTTTTTTTTTTTTTTTTTTTTTT
    TTTTTTTTTT


    :param fasta: multi-fasta file with consensus seqeunces
    :param recoded_fasta: recoded consensus multi fasta file with D replaced with 1 and [T, -] replaced with 0
    :return: list of UniProt accession numbers
    """

    # List to contain accessions number
    acc = []

    # Open fasta file for reading and new recoded file for 
    # recoding
    with open(fasta, 'r') as f, \
         open(recoded_fasta, 'w') as f1:
        
        # For each line in fasta strip the new lines
        for line in f:
            line = line.strip()

            # collect accessions and write headers
            if line.startswith('>'):
                f1.write(line + '\n')
                line_split = line.split(' ')
                acc.append(line_split[1].strip('acc='))
            
            # recode sequences and write to new file
            else:
                line_recoded = line.replace('-', '0').replace('D', '1').replace('T', '0')
                f1.write(line_recoded + '\n')
    
    return acc


        
                
def main():

    # Parse consensus fasta to grab accessions and recode fasta
    accs = parse_consensus('consensus_IDR.txt', 'recoded_IDR.txt')
    
    # create new directory
    os.makedirs('UniProt_data')

    
    for acc in accs:
        subprocess.run(['wget', '-P', 'UniProt_data', f'https://rest.uniprot.org/uniprotkb/{acc}.fasta'])

if __name__ == '__main__':
    main()


