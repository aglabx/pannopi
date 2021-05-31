rule quast:
    input:
        assembly = rules.contera.output,
        ref = config["reference_file"]
    conda:
        envs.quast
    output:
        config["quast_out_file"]
    params:
        directory(config["quast_dir"])
    shell:
        """
        quast -o {params} \
        -r {input.ref} {input.assembly}
        """
