rule busco:
    input:
        anno_faa = rules.annotation.output.annotation_faa
    conda:
        envs.busco
    threads: workflow.cores
    output:
        busco_outfile = config["busco_outfile"]
    params:
        db = locals.busco_db_downloads,
        folder_to_run = directory(config["busco_run_dir"]),
        outdir = "busco"
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
             --download_path {params.db}
             """  
