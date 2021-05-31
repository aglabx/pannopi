rule mlst:
    input:
        assembly_filtered = rules.contera.output
    output:
        config["mlst"]
    threads: 1
    conda:
        envs.mlst
    shell:
        """
        mlst {input} > {output}
        """
