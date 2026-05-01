
def parse_consensus(fasta: str) -> tuple[list[str], list[str]]:
    """Parses consensus IDR data from DisProt. Consensus sequences have the
    following format.

    >disprot|DP00004|full acc=P49913
    --------------------------------------------------------------------------------
    -----------------------------------------------------TTTTTTTTTTTTTTTTTTTTTTTTTTT
    TTTTTTTTTT

    :param fasta: multi-fasta file with consensus seqeunces
    :return: tuple with two elements: list containing UniProt accessions numbers 
    & a list containing sequences. 
    """

    acc = []

    with open(fasta, 'r') as f:
        for line in f:
            line = line.strip()

            # collect accessions
            if line.startswith('>'):
                line_split = line.split(' ')
                acc.append(line_split[1].strip('acc='))
                
            
parse_consensus('consensus_IDR.txt')

