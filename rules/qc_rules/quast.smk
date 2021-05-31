rule quast:
    input:
        assembly = rules.contera.output
    conda:
        envs.quast
    output:
        config["quast_out_file"]
    params:
        directory(config["quast_dir"])
    shell:
        """
        quast -o {params} \
        {input}
        """
