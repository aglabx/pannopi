rule quast:
    input:
        assembly = rules.assembly.output.assembly
        ref = config["reeference_file"]
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