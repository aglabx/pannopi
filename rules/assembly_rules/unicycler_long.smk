rule assembly:
    input:
        long_reads = config["long_reads_file"]
    conda:
        envs.unicycler
    threads: workflow.cores
    output:
        assembly = config["assembly"],
    params:
        dir = directory(config["assembly_dir"])
    shell:
        "unicycler -l {input.long_reads} -t {threads} -o {params.dir}"
