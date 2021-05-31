rule all:
    input:
        results_file = config["results_file"]
    log: config["pannopi_log"]
    benchmark: config["pannopi_bench"]
    
include: "settings.snakefile"

include: "../rules/prepare.smk"

include: "../rules/assembly_rules/unicycler_short.smk"

if locals.blastn_db != "False":
    include: "../rules/qc_rules/contera_aio.smk"
else:
    include: "../rules/qc_rules/contera_adapters.smk"

include: "../rules/structural_annotation.smk"

if config["reference_file"] == "False":
    include: "../rules/qc.smk"
else:
    include: "../rules/qc_ref.smk"

include: "../rules/functional_annotation.smk"

if config["reference_file"] == "False":
    include: "../rules/results.smk"
else:
    include: "../rules/results_ref.smk"
