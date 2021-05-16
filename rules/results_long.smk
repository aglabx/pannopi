rule results:
    input:
        assembly = rules.assembly.output.assembly,
        egg = rules.eggnog.output,
        quast = rules.quast.output,
        whole_report = rules.abricate_summary.output,
    output:
        results_file = config["results_file"],
    params:
        path = directory(config["results_path"])
    shell:
        "cp {input} {params}"
