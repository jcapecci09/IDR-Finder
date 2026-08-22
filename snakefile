rule all:
    input:
        'Data/test_uniprot.fasta'

rule disprot_encoder:
    input:
        'consensus_IDR.txt'
    
    output:
        directory('Data')
    
    shell:
        '''
        mkdir Data
        DisProtEncoder -i {input} -o {output} -w 16
        '''

rule split_fastas:
    input:
        recoded='Data/consensus_IDR_recoded.txt',
        uniprot='Data/UniProt.fasta'
    output: 
        test='Data/test_uniprot.fasta',
        train='Data/train_uniprot.fasta',
        val='Data/validation_uniprot.fasta',
        test1='Data/test_recoded.fasta',
        train1='Data/train_recoded.fasta',
        val1='Data/validation_recoded.fasta'
        
    shell:
        '''
        fasta-splitter -i {input.uniprot} --validation \
        -t {output.test} -o {output.train} -v {output.val} \
        -r 42
        fasta-splitter -i {input.recoded} --validation \
        -t {output.test1} -o {output.train1} -v {output.val1} \
        -r 42
        '''
