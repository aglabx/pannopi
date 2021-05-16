rule mlst:
    input:
        assembly_filtered = rules.assembly.output.assembly
    output:
        config["mlst"]
    conda:
        envs.mlst
    shell:
        """
        mlst {input} > {output}
        """