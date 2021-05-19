rule mlst:
    input:
        assembly_filtered = rules.assembly.output.assembly
    output:
        config["mlst"]
    threads: 1
    conda:
        envs.mlst
    shell:
        """
        mlst {input} > {output}
        """