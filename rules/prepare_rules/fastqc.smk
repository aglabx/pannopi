rule fastqc1:
    input:
        forward_read = config["v2trim_in_file1"],
        rewerse_read = config["v2trim_in_file2"]
    conda:
        envs.fastqc
    threads: workflow.cores - 1
    output:
        fastq_file_1 = config["fastqc_file1"],
    params:
        fastqc1_dir = directory(config["fastqc1_dir"])
    shell:
        """
        fastqc \
            -o {params.fastqc1_dir} \
            -t {threads} \
            {input}
        """

rule fastqc2:
    input:
        rules.rmdup.output.rmdup_out_forward,
        rules.rmdup.output.rmdup_out_reverse
    conda:
        envs.fastqc
    threads: workflow.cores - 1 
    output:
        fastq_file_2 = config["fastqc_file2"]
    params:
        fastqc2_dir = directory(config["fastqc2_dir"])
    shell:
        """
        fastqc \
            -o {params.fastqc2_dir} \
            -t {threads} \
            {input}
        """
