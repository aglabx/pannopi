rule eggnog:
    input:
        prokka_faa = rules.annotation.output.annotation_faa
    conda:
        envs.eggnog
    threads:
        workflow.cores
    log: config["eggnog_log"]
    benchmark: config["eggnog_bench"]
    output:
        eggnog_out_annotation = config["eggnog_out_annotation"], 
        eggnog_out_orthologs = config["eggnog_out_orthologs"],
    params:
        eggnog_db = locals.eggnog_db,
        eggnog_prefix = config["eggnog_prefix"],
        eggnog_dir = config["eggnog_dir"]
    shell:
        """
        emapper.py \
          -i {input.prokka_faa} \
          -m diamond \
          --cpu {threads} \
          --data_dir {params.eggnog_db} \
          --output {params.eggnog_prefix} \
          --output_dir {params.eggnog_dir} \
          --report_orthologs 2> {log} | tee -a {log}
        """
