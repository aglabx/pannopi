rule fastani:
    input:
        assembly = rules.assembly.output.assembly,
        ref = config["reference_file"]
    conda:
        envs.fastani
    output:
        config["fastani_outfile"]
    params:
        fastani_dir = directory(config["fastani_dir"])
    shell:
        """
        fastANI -q {input.assembly} -r {input.ref} -o {output}
        """
