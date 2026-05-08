"""I've first decided to create a naive model 

Author: Jcapecci09
"""

import re


def disorder_finder(seq: str) -> str:

    # define scoring matrix
    # Amino acids with disorder promoting regions = 1
    # Amino acids with order promoting regions = -1
    # Amino acids not associated with either = 0 
    scoring_matrix = {
    'A': 1,  'R': 1,  'N': -1, 'D': 0,  'C': -1,
    'Q': 1,  'E': 1,  'G': 1,  'H': 0,  'I': -1,
    'L': -1, 'K': 1,  'M': 0,  'F': -1, 'P': 1,
    'S': 1,  'T': 0,  'W': -1, 'Y': -1, 'V': -1
    }

    # find length of sequence then initalize score and recoded sequence
    length = len(seq)
    score = 0
    recoded = ''
    size = 4

    # Find the position for each amino acid
    for indx in range(length): 

        # Takes care of edge case at front of sequence
        if indx - size < 0:
            first = 0
        else:
            first = indx - size

        # Takes care of edge case at end of sequence 
        if indx + size > length:
            last = length
        else:
            last = indx + size
        
        # Find the window
        # 3 amino acids before and 3 amino acids after current
        window = seq[first:last]
        
        # For each amino acid in the window add its
        # disorder score to the window score
        for letter in window:
            score += scoring_matrix[letter]
            
        
        # If the score / len(window) is 75% 
        # its a 'disordered amino acid'
        if score / len(window) >= 0.75:
            recoded += '1'
            score = 3
        
        # else its 'ordered'
        else:
            recoded += '0'
            score = 0


    # Remove any disordered regions with 4 or less amino acids
    smoothing = re.sub(
        r'(?<!1)1{1,7}(?!1)', # pattern for 4 or less amino acids
        lambda m: '0' * len(m.group()), # replace regions with '0'
        recoded # perform operation on recoded
    )

    return smoothing


def main():
    with open('Data/UniProt.fasta', 'r') as f:
        fastas = []
        fasta = ''
        f.readline()
        for line in f:
            line = line.strip()
            if not line.startswith('>'):
                fasta += line
            else:
                fastas.append(fasta)
                fasta = ''
        
        fastas.append(fasta)
    
    print(fastas[1])
    print(disorder_finder(fastas[1]))
                


if '__main__' == __name__:
    main()
