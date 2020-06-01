configfile: "config/config.yaml"

rule all:
    input:
        results_file = config["results_file"]

rule tools:
    params:
        v2trim = "tools/v2trim/V2_trim.exe",
        ill_ext = "tools/v2trim/illumina_ext.data",
        rmdub = "tools/rmdub/rmdup.exe",
        contera = "tools/contera/contera.py",
        eggnog = "/mnt/projects/vdikaya/Tools/eggnog-mapper-1.0.3/emapper.py", # придумать как ставить еггног
        blast_db = "/mnt/projects/shared/ncbi/blast/db/nt", # тоже придумать
        goobo = "tools/goanno/GOanno.py",
        obo_annotation = "tools/goanno/go.obo",

tools = rules.tools.params

rule envs:
    params:
        abricate = "../envs/abricate.yaml",
        fastqc = "../envs/fastqc.yaml",
        mlst = "../envs/mlst.yaml",
        prokka = "../envs/prokka.yaml",
        r = "../envs/r.yaml",
        skesa = "../envs/skesa.yaml",
        unicycler = "../envs/unicycler.yaml",
        blast = "../envs/blast.yaml",
        jellyfish = "../envs/jellyfish.yaml",
        ncbidown = "../envs/ncbi-download.yaml",
        quast = "../envs/quast.yaml",
        samtools = "../envs/samtools.yaml",
        spades = "../envs/spades.yaml",
        
envs = rules.envs.params

include: "rules/prepare.sf"

include: config["assembler"]

include: "rules/cleaning.sf"

include: config["annotator"]

include: "rules/qc.sf"

include: "rules/functional_annotation.sf"


