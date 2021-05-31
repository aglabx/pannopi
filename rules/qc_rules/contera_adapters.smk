rule contera:
    input:
        assembly = rules.assembly.output.assembly
    conda:
        envs.contera
    threads: workflow.cores
    output:
        config["contera_out_file"]
    params:
        directory(config["contera_dir"])
    shell:
        """
        contera -a {input.assembly} -t {threads} -o {params}
        """
