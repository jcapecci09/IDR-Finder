"""Script to extract data from DisProt and create two files: 

1. Recoded DisProt fasta file
2. corresponding UniProt fasta file

Author: jcapecci09
"""

from pathlib import Path
import os
from concurrent.futures import ThreadPoolExecutor
import requests
import time

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


def download(url: str):
    """Download fasta data from a UniProt URL.

    :param url: UniProt fasta URL
    :return: Fasta text if successful, otherwise None
    """

    # Extract filename from URL
    filename = url.split('/')[-1]
    
    try:

        # Send GET request with timeout to avoid hanging forever
        r = requests.get(url, timeout=10)
        
        # Check if request succeeded and response contains data
        if r.status_code == 200 and r.content:

            # Print successful download
            print(f"downloading data from: {url}")

            # Return fasta text
            return r.text
        else:

            # Print failed request status code
            print(f"Failed: {url} ({r.status_code})")
            return None
         
    except Exception as e:

        # Catch connection/time out errors without crashing program
        print(f"Error: {url} -> {e}")
        return None
        
                
def main():

    # Make directory to hold data
    os.makedirs('Data', exist_ok=True)

    # Parse consensus fasta to grab accessions and recode fasta
    accs = parse_consensus('consensus_IDR.txt', 'Data/consensus_IDR_recoded.txt')
    
    # Collect URLS in list
    urls = [f'https://rest.uniprot.org/uniprotkb/{acc}.fasta' for acc in accs]


    # Download data faster
    # Program spends most of its time waiting for network responses
    # ThreadPoolExecutor allows multiple URL downloads to happen concurrently
    # While one thread waits for a response, another can download data
    if not Path('Data/UniProt.fasta').exists():

        # define number of workers 
        num_workers = 32
        start = time.perf_counter()

        # Create a pool of worker threads to download URL's concurrently
        with ThreadPoolExecutor(max_workers=num_workers) as executer:

            # Map each URL to the download function
            # Returns downloaded fasta contents in order
            results = list(executer.map(download, urls))

        end = time.perf_counter()

        # Print total download time
        print(f'Time to download data: {(end - start):.2f}s with {num_workers} workers')

        # Combine all fasta data into one fasta file
        with open('Data/UniProt.fasta', 'w') as f:
            for fasta in results:

                # Skip failed downloads that returned None
                if fasta:
                    f.write(fasta)

        print('data retrieved')
    
    # If directory already contains data, don't bother downloading
    else:
        print('Data already retrieved')

if __name__ == '__main__':
    main()
