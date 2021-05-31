rule contera:
    input:
        assembly = rules.assembly.output.assembly
    conda:
        envs.contera
    threads: workflow.cores
    output:
        config["contera_out_file"]
    params:
        outdir = directory(config["contera_dir"]),
        blast_db = locals.blastn_db
    shell:
        """
        contera -m aio -a {input.assembly} -db {params.blast_db} -t {threads} -o {params.outdir}
        """
