rule fastqc1:
    input:
        forward_read = config["raw_fastq_1"],
        rewerse_read = config["raw_fastq_2"]
    conda:
        envs.fastqc
    output:
        fastq_file_1 = config["fastqc_file1"],
    params:
        fastqc1_dir = directory(config["fastqc1_dir"])
    shell:
        """
        fastqc \
            -o {params.fastqc1_dir} \
            -t 32 \
            {input}
        """

rule fastqc2:
    input:
        rules.rmdub.output.rmdub_out_file1,
        rules.rmdub.output.rmdub_out_file2
    conda:
        envs.fastqc
    output:
        fastq_file_2 = config["fastqc_file2"]
    params:
        fastqc2_dir = directory(config["fastqc2_dir"])
    shell:
        """
        fastqc \
            -o {params.fastqc2_dir} \
            -t 32 \
            {input}
        """