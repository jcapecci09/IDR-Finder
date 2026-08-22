#  Take fasta file
# Convert it to pandas dataframe

import pandas as pd
from multifasta_collector import mfc
import argparse



def collector(dictionary, label):

    aa_collector = []
    acc_collector = []
    pos_collector = []
    for key, value in dictionary.items():

        if label == 'Amino Acid':
            acc = key.split('|')[1]
        elif label == 'Order':
            acc = key.split('=')[1]

        aa = [i for i in value]
        accs = [acc for i in range(len(aa))]
        pos = [i + 1 for i in range(len(aa))]
        aa_collector.extend(aa)
        acc_collector.extend(accs)
        pos_collector.extend(pos)
        

    df = pd.DataFrame({
        "Acc": acc_collector,
        label: aa_collector,
        'Pos': pos_collector
    })

    return df

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--uniprot', nargs='+', required=True)
    parser.add_argument('--recoded', nargs='+', required=True)
    parser.add_argument('--outputs', nargs='+', required=True)
    args = parser.parse_args()

    for uniprot_file, recoded_file, output in zip(args.uniprot, args.recoded, args.outputs):

        uniprot_d =  mfc(uniprot_file)
        recoded_d = mfc(recoded_file)

        new_uniprot = {}
        new_recoded = {}

        for (key, seq), (key1, seq1) in zip(uniprot_d.items(), recoded_d.items()):

            if len(seq) == len(seq1):
                new_uniprot[key] = seq
                new_recoded[key1] = seq1

        uniprot_d = new_uniprot
        recoded_d = new_recoded

        df = collector(new_uniprot, 'Amino Acid')
        df1 = collector(new_recoded, 'Order')

        df_merge = pd.merge(
            df,
            df1,
            on=['Acc', 'Pos'],
            how='inner'
        )
        df_merge.to_csv(output, index=False)

if __name__ == '__main__':
    main()
