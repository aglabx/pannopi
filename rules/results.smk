rule results:
    input:
        assembly = rules.assembly.output.assembly,
        assembly_filtered = rules.contera.output,
        scope = rules.genomescope.output,
        fast1 = rules.fastqc1.output,
        fast2 = rules.fastqc2.output,
        quast = rules.quast.output,
        proteins = rules.annotation.output.annotation_faa,
        functional_annotation = rules.eggnog.output.eggnog_out_annotation,
        busco = rules.busco.output.busco_outfile,
        whole_report = rules.abricate_summary.output,
    output:
        results_file = config["results_file"],
    params:
        path = directory(config["results_path"])
    shell:
        "cp {input} {params}"
