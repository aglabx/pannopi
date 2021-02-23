rule blastn:
    input:
        rules.assembly.output.assembly,
    conda:
        envs.blast
    threads: workflow.cores * 0.5
    output:
        blastn_out = config["blastn_out"]
    params:
        blast_db = config["blast_db"]
    shell:
        """
        blastn \
            -query {input} \
            -db {params.blast_db} \
            -max_target_seqs 5 \
            -outfmt '6 qseqid sseqid pident qstart qend length evalue sscinames staxids' \
            -evalue 1e-5 \
            -perc_identity 90 \
            -num_threads {threads} \
            -out {output}
        """

rule contera:
    input:
        scaffold = rules.assembly.output.assembly,
        blast_in = rules.blastn.output
    output:
        assembly_filtered = config["assembly_filtered"],
        adapters_report = config["adapters_report"],
        report = config["contera_report"]
    params:
        contera_path = tools.contera,
        outdir = directory(config["contera_dir"]),
        adapters = tools.contera.replace("contera.py", "adapters_db/adaptor_fasta.fna")
    shell:
        """
        {params.contera_path} \
            -s {input.scaffold} \
            -b {input.blast_in} \
            -a {params.adapters} \
            -o {params.outdir}
        """
