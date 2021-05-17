rule assembly:
    input:
        long_reads = config["long_reads_file"],
        forward_reads = rules.rmdup.output.rmdup_out_forward,
        reverse_reads = rules.rmdup.output.rmdup_out_reverse,
    conda:
        envs.unicycler
    threads: workflow.cores
    output:
        assembly = config["assembly"],
    params:
        dir = directory(config["assembly_dir"])
    shell:
        """
        unicycler -1 {input.forward_reads} -2 {input.reverse_reads} -l {input.long_reads} -t {threads} --no_pilon -o {params}
        """