rule fastani:
    input:
        assembly = rules.assembly.output.assembly,
        ref = config["reference_file"]
    conda:
        envs.fastani
    threads: 1
    output:
        config["fastani_outfile"]
    log: config["fastani_log"]
    benchmark: config["fastani_bench"]
    params:
        fastani_dir = directory(config["fastani_dir"])
    shell:
        """
        fastANI -q {input.assembly} -r {input.ref} -o {output} 2> {log} | tee -a {log}
        """
