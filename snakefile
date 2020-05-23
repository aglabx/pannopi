configfile: "config/config.yaml"

rule all:
    input:
        res_spad = config["results_spad_file"],
        res_uni = config["results_uni_file"]
        
rule tools:
    params:
        v2trim = "tools/v2trim/V2_trim.exe",
        ill_ext = "tools/v2trim/illumina_ext.data",
        rmdub = "tools/rmdub/rmdup.exe",
        contera_path = "tools/contera/contera.py",
        eggnog_path = "/mnt/projects/vdikaya/Tools/eggnog-mapper-1.0.3/emapper.py", # придумать как ставить еггног
        blast_db = "/mnt/projects/shared/ncbi/blast/db/nt", # тоже придумать
        goobo = "tools/goanno/GOanno.py",
        obo_annotation = "tools/goanno/go.obo",

include: "rules/prepare.sf"

include: config["assembler"]

include: "rules/cleaning.sf"

include: config["annotator"]

include: "rules/functional_annotation.sf"

include: "rules/qc.sf"
