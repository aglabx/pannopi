rule assembly:
    input:
        forward_reads = rules.v2trim.output.v2trim_out_forward,
        reverse_reads = rules.v2trim.output.v2trim_out_reverse,
    conda:
        envs.unicycler
    threads: min(workflow.cores, 32)
    log: config["unicycler_log"]
    benchmark: config["unicycler_bench"]
    output:
        assembly = config["assembly"],
    params:
        dir = directory(config["assembly_dir"])
    shell:
        "unicycler -1 {input.forward_reads} -2 {input.reverse_reads} -t {threads} -o {params} 2> {log} | tee -a {log}"
