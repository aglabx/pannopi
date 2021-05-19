rule busco:
    input:
        anno_faa = rules.annotation.output.annotation_faa
    conda:
        envs.busco
    threads: workflow.cores
    output:
        busco_outfile = config["busco_outfile"]
    log: config["busco_log"]
    benchmark: config["busco_bench"]
    params:
        db = locals.busco_db_downloads,
        folder_to_run = directory(config["busco_run_dir"]),
        outdir = "busco",
        busco_summary = config["busco_summary"]
    shell:
       """
       cd {params.folder_to_run}
       
       busco \
             --auto-lineage-prok \
             -i {input.anno_faa} \
             -o {params.outdir} \
             -m prot \
             -f \
             -c {threads} \
             --download_path {params.db} 2> {log} | tee -a {log}
             
        mv {params.busco_summary} {output.busco_outfile}
             """  
