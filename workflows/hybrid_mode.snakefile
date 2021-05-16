configfile: "config/config.yaml"

rule all:
    input:
        results_file = config["results_file"]

rule locals:
    params:
       busco_db = "",
       blastn_db = "",
       eggnog_db = ""

locals = rules.locals.params

rule tools:
    params:
        contera = "tools/contera/contera.py",
        eggnog = "/media/eternus1/projects/zilov/soft/eggnog-mapper-2.0.4-rf1/emapper.py", # придумать как ставить еггног
        eggnog_db = "/mnt/projects/zilov/soft/eggnog-mapper-2.0.4-rf1/database",
        blast_db = "/mnt/projects/shared/ncbi/blast/db/nt", # тоже придумать
        goobo = "tools/goanno/GOanno.py",
        obo_annotation = "tools/goanno/go.obo",
        genomescope = "tools/genomescope/genomescope.R"

tools = rules.tools.params

rule envs:
    params:
        abricate = "../../envs/abricate.yaml",
        fastqc = "../../envs/fastqc.yaml",
        mlst = "../../envs/mlst.yaml",
        prokka = "../../envs/prokka.yaml",
        r = "../../envs/r.yaml",
        skesa = "../../envs/skesa.yaml",
        unicycler = "../../envs/unicycler.yaml",
        blast = "../../envs/blast.yaml",
        jellyfish = "../../envs/jellyfish.yaml",
        ncbidown = "../../envs/ncbi-download.yaml",
        quast = "../../envs/quast.yaml",
        samtools = "../../envs/samtools.yaml",
        spades = "../../envs/spades.yaml",
        v2trim = "../../envs/v2trim.yaml",
        rmdup = "../../envs/rmdup.yaml",
        busco = "../../envs/busco.yaml",
        fastani = "../../envs/fastani.yaml",
        eggnog = "../../envs/eggnog.yaml"

envs = rules.envs.params

include: "../rules/prepare.smk"

include: "../rules/assembly_rules/unicycler_hybrid.smk"

#include: "../rules/cleaning.smk"

include: "../rules/structural_annotation.smk"

if config["reference_file"] == "False":
    include: "../rules/qc.smk"
else:
    include: "../rules/qc_ref.smk"

include: "../rules/functional_annotation.smk"

include: "../rules/results.smk"
