rule assembly:
    input:
        long_reads = config["long_reads_file"]
    conda:
        envs.unicycler
    threads: workflow.cores
    log: config["unicycler_log"]
    benchmark: config["unicycler_bench"]
    output:
        assembly = config["assembly"],
    params:
        dir = directory(config["assembly_dir"])
    shell:
        "unicycler -l {input.long_reads} -t {threads} -o {params.dir} 2> {log} | tee -a {log}"
