
rule envs:
    params:
        abricate = "../../envs/abricate.yaml",
        fastqc = "../../envs/fastqc.yaml",
        mlst = "../../envs/mlst.yaml",
        prokka = "../../envs/prokka.yaml",
        contera = "../../envs/contera.yaml",
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
        eggnog = "../../envs/eggnog.yaml",
        genomescope = "../../envs/genomescope.yaml"
        
envs = rules.envs.params

rule locals:
    params:
       blastn_db = "/media/eternus1/data/ncbi/blast/db/nt",
       eggnog_db = "/media/eternus1/nfs/projects/shared/databases/eggnog_database_212",
       busco_db_downloads = "/media/eternus1/nfs/projects/shared/databases/busco"

locals = rules.locals.params
