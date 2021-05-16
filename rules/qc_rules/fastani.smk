rule quast:
    input:
        assembly = rules.assembly.output.assembly
        ref = config["reeference_file"]
    conda:
        envs.quast
    output:
        config["fastani_outfile"]
    params:
        fastani_dir = directory(config["fastani_dir"])
    shell:
        """
        fastani -i {input.assembly} -r {input.ref} -o {output}
        """