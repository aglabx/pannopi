rule results:
    input:
        assembly_filtered = rules.assembly.output.assembly,
        egg = rules.eggnog.output,
        scope = rules.genomescope.output,
        fast1 = rules.fastqc1.output,
        fast2 = rules.fastqc2.output,
        quast = rules.quast.output,
        whole_report = rules.abricate_sumary.output,
        goann = rules.goann.output,
    output:
        results_file = config["results_file"],
    params:
        path = directory(config["results_path"])
    shell:
        "cp {input} {params}"