rule all:
    input:
        test_csv = 'Data/csv_datasets/test_csv',
        train_csv = 'Data/csv_datasets/train_csv',
        val_csv = 'Data/csv_datasets/val_csv'

rule disprot_encoder:
    input:
        'consensus_IDR.txt'
    
    output:
        directory('Data/encoded')
    
    shell:
        '''
        mkdir Data
        DisProtEncoder -i {input} -o {output} -w 16
        '''

rule split_fastas:
    input:
        recoded='Data/encoded/consensus_IDR_recoded.txt',
        uniprot='Data/encoded/UniProt.fasta'
    output: 
        test='Data/fasta/test_uniprot.fasta',
        train='Data/fasta/train_uniprot.fasta',
        val='Data/fasta/validation_uniprot.fasta',
        test1='Data/fasta/test_recoded.fasta',
        train1='Data/fasta/train_recoded.fasta',
        val1='Data/fasta/validation_recoded.fasta'
        
    shell:
        '''
        fasta-splitter -i {input.uniprot} --validation \
        -t {output.test} -o {output.train} -v {output.val} \
        -r 42
        fasta-splitter -i {input.recoded} --validation \
        -t {output.test1} -o {output.train1} -v {output.val1} \
        -r 42
        '''

rule prepare_datasets:
    input:
        test='Data/fasta/test_uniprot.fasta',
        train='Data/fasta/train_uniprot.fasta',
        val='Data/fasta/validation_uniprot.fasta',
        test1='Data/fasta/test_recoded.fasta',
        train1='Data/fasta/train_recoded.fasta',
        val1='Data/fasta/validation_recoded.fasta'
    output:
        test_csv = 'Data/csv_datasets/test_csv',
        train_csv = 'Data/csv_datasets/train_csv',
        val_csv = 'Data/csv_datasets/val_csv'
    shell: 
        '''
        python format_data.py \
        --uniprot {input.test} {input.train} {input.val} \
        --recoded {input.test1} {input.train1} {input.val1} \
        --outputs {output.test_csv} {output.train_csv} {output.val_csv}
        '''
        
