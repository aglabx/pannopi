#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 30.05.2021
# @author: Danil Zilov
# @contact: zilov.d@gmail.com

import argparse
import os
from inspect import getsourcefile


def set_db_paths(locals_settings_file, eggnogdb_dir, blastdb_dir):
    busco_db = os.path.normpath(os.path.join(eggnogdb_dir, "../busco"))
    with open(locals_settings_file, "w") as fw:
        locals_settings = f"""
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
        contera = "../../envs/contera.yaml",
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
       blastn_db = "{blastdb_dir}",
       eggnog_db = "{eggnogdb_dir}",
       busco_db_downloads = "{busco_db}"

locals = rules.locals.params
        """
        fw.write(locals_settings)
        return "\nAll paths to databases is set! Now you can run Pannopi!\n"


def download_eggnog(outdir):
    eggnog_data_dir = os.path.join(outdir, "eggnog")
    eggnog_db = os.path.join(eggnog_data_dir, "eggnog_proteins.dmnd")
    cmd = f"download_eggnog_data.py --data_dir {eggnog_data_dir} -y"
    if not os.path.exists(eggnog_data_dir):
        os.makedirs(eggnog_data_dir)
        os.system(cmd)
        return eggnog_data_dir
    elif os.path.exists(eggnog_db):
        print("\nEggnog database already downloaded, continue...\n")
        return eggnog_data_dir



def download_blast(outdir):
    blast_nt_url = "https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz"
    blastnt_data_dir = os.path.join(outdir, "blastnt")
    blast_db = os.path.join(blastnt_data_dir, "nt")
    if not os.path.exists(blastnt_data_dir):
        os.makedirs(blastnt_data_dir)
    elif os.path.exists(blast_db):
        print("\nBLAST database already downloaded, continue...\n")
        return blast_db
    cmd = (
        f'cd {blastnt_data_dir} && '
        f'echo Download blast database..'
        f'wget -nH --user-agent=Mozilla/5.0 --relative --no-parent --reject "index.html*" --cut-dirs=4 -e robots=off -O nt.gz {blast_nt_url} && '
        f'echo Decompressing... && '
        f'gunzip nt.gz && '
        f'echo Build database... &&'
        f'makeblastdb -dbtype nucl -in nt'
    )
    os.system(cmd)
    return blast_db


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Database downloader for Pannopi. '
                                                 'Eggnog, blast and all modes needs only outdir; '
                                                 'To set your database use set mode with -e and -b arguments')
    parser.add_argument('-m', '--mode', help="mode to use [default = eggnog ~ 50GB], all databases is ~160 GB",
                        choices=["all", "set", "eggnog", "blast"], default="short")
    parser.add_argument('-o', '--outdir', help="directory to download databases", required=False, default=False)
    parser.add_argument('-e', '--eggnogdb', help="path to eggnog database folder", required=False, default=False)
    parser.add_argument('-b', '--blast', help="path to blast nucleotide (nt) database", required=False, default=False)

    args = vars(parser.parse_args())

    mode = args["mode"]
    outdir = args["outdir"]
    eggnog_db_dir = args["eggnogdb"]
    blast_db_dir = args["blast"]

    execution_folder = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
    settings_file = os.path.normpath(os.path.join(execution_folder, "../workflows/settings.snakefile"))

    if mode == "set":
        if not eggnog_db_dir and not blast_db_dir:
            parser.error("\nTo set db you should provide at least one path for eggnog or blast database!\n")
        if eggnog_db_dir:
            eggnog_db_dir = os.path.abspath(eggnog_db_dir)
        if blast_db_dir:
            blast_db_dir = os.path.abspath(blast_db_dir)
            
    elif mode != "set":
        if not outdir:
            parser.error("\nTo download db you should provide a path to output directory!\n")
        outdir = os.path.abspath(outdir)
        if mode == "eggnog" or mode == "all":
            eggnog_db_dir = download_eggnog(outdir)
        if mode == "blast" or mode == "all":
            blast_db_dir = download_blast(outdir)

    print(set_db_paths(settings_file, eggnog_db_dir, blast_db_dir))
