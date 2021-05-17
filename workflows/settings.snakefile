rule locals:
    params:
       blastn_db = "/mnt/projects/shared/ncbi/blast/db/nt",
       eggnog_db = "/mnt/projects/databases/eggnog_database_212",
       busco_db_downloads = "/mnt/projects/databases/busco" # folder in which busco will store databases

locals = rules.locals.params

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
        eggnog = "../../envs/eggnog.yaml",
        genomescope = "../../envs/genomescope.yaml"
        
envs = rules.envs.params