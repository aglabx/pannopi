rule results:
    input:
        assembly = rules.assembly.output.assembly,
        egg = rules.eggnog.output,
        quast = rules.quast.output,
        busco = rules.busco.output.busco_outfile,
        proteins = rules.annotation.output.annotation_faa,
        whole_report = rules.abricate_summary.output,
        fastani = rules.fastani.output,
    output:
        results_file = config["results_file"],
    params:
        path = directory(config["results_path"])
    shell:
        "cp {input} {params}"