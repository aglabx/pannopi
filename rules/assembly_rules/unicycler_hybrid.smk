rule assembly:
    input:
        forward_reads = rules.rmdub.output.rmdub_out_file1,
        reverse_reads = rules.rmdub.output.rmdub_out_file2,
        long_reads = config["long_reads_file"]
    conda:
        envs.unicycler
    threads: workflow.cores
    output:
        assembly = config["assembly"],
    params:
        dir = directory(config["assembly_dir"])
    shell:
        "unicycler -1 {input.forward_reads} -2 {input.reverse_reads} -l {input.long_reads}-t {threads} -o {params}"
