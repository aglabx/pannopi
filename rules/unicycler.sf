rule assembly:
    input:
        forward_reads = rules.rmdub.output.rmdub_out_file1,
        reverse_reads = rules.rmdub.output.rmdub_out_file2
    conda:
        envs.unicycler
    threads: workflow.cores
    output:
        assembly = config["assembly"],
        assembly_gfa = config["assembly_gfa"],
    params:
        dir = directory(config["assembly_dir"])
    shell:
        "unicycler -1 {input.forward_reads} -2 {input.reverse_reads} -t {threads} -o {params}"
