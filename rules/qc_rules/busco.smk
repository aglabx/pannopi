rule busco:
    input:
        assembly = rules.assembly.output.assembly
    conda:
        envs.busco
    output:
        busco_outfile = config["busco_outfile"]
    threads: workflow.cores
    params:
        db = locals.busco_db
    shell:
       """busco \
             --auto-lineage-prok \
             --config /home/dzilov/soft/busco5/config/config.ini \
             -i /mnt/data/vgp/glis_glis/GCA_004024805.1_XerIna_v1_BIUU_genomic.fna \
             -c 150 \
             -m geno \
             -f \
             --out GCA_004024805.1_XerIna_v1_BIUU_genomic_result
             """  
