rule assembly:
    input:
        forward_reads = rules.rmdup.output.rmdup_out_forward,
        reverse_reads = rules.rmdup.output.rmdup_out_reverse
    conda:
        envs.unicycler
    threads: workflow.cores
    output:
        assembly = config["assembly"],
    params:
        dir = directory(config["assembly_dir"])
    shell:
        "unicycler -1 {input.forward_reads} -2 {input.reverse_reads} -t {threads} -o {params}"
