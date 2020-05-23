configfile: "config/config.yaml"

rule all:
    input:
        contera_report = config["contera_report"],
        qc = config["quast_out_file"],
        scope_file = config["scope_file"],
        fastq_file_2 = config["fastqc_file2"]
        fastq_file_1 = config["fastqc_file1"]

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

#include: config["annotator"]

#include: "rules/functional_annotation.sf"

include: "rules/qc.sf"
