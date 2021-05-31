#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: <data>
# @author: <name>
# @contact: <email>

import argparse
import os
import os.path
from inspect import getsourcefile
from datetime import datetime
import string
import random

def check_for_databases(settings_file):
    if not os.path.exists(settings_file):
        raise ValueError("\nPannopi requires eggnog-database, please download or set it "
                         "with pannopi_download_db.py!\n")
    else:
        return True
#         ask_for_database = input("Pannopi requires eggnog-database (~50GB), do you wanna download it? [y/n]: ")
#         if ask_for_database == "y":
#             ask_for_outdir = input("Where do you wanna install it? Provide path to folder to store database: ")
#             if ask_for_outdir:
#                 output = ask_for_outdir
#             ask_for_blast_db = input("Do you want to download blastn database to filter your assembly (~100GB)? [y/n]: ")
#             if ask_for_blast_db == "y":
#                 run = f"pannopi_download_db.py -m all -o {output}"
#             else:
#                 run = f"pannopi_download_db.py -o {output}"
#             os.system(run)
#             return True
#         else:
#             ask_if_it_installed = input("Do you wanna provide path path to eggnog-database? [y/n]: ")
#             if ask_if_it_installed == "y":
#                 path_to_eggnog = ""
#
#     else:
#         return True
#
# def check_for_blast_db(settings_file):
#     if not os.path.exists(settings_file):
#         ask_for_database = input("Pannopi needs blastn database to make assembly-content report (~110GB), do you wanna download it? [y/n]: ")
#         if ask_for_database == "y":
#             ask_for_outdir = input("Where do you wanna install it? Provide path to folder to store database: ")
#             if ask_for_outdir:
#                 output = ask_for_outdir
#             if ask_for_blast_db == "y":
#                 run = f"pannopi_download_db.py -m all -o {output}"
#             else:
#                 run = f"pannopi_download_db.py -o {output}"
#             os.system(run)
#             return True
#         else:
#             ask_if_it_installed = input("Do you have blast nt database installed on your system? [y/n]: ")
#             if ask_if_it_installed == "y":
#                 path_to_blast = input("Provide path path to blast nt database: ")
#
#             raise ValueError(
#                 "Pannopi requires eggnog-database, please download or set it with pannopi_download_db.py!")

def config_short(forward_read, reverse_read, reference_fasta, prefix, outdir, mode, execution_folder, config_file):
    #Config-maker run
    command = f"{execution_folder}/scripts/config-maker.py -1 {forward_read} -2 {reverse_read} " \
              f"-r {reference_fasta} -p {prefix} -o {outdir} -m {mode} -c {config_file}"
    print(command)
    os.system(command)


def config_long(long_read,reference_fasta, prefix, outdir, mode, execution_folder, config_file):
    #Config-maker run
    command = f"{execution_folder}/scripts/config-maker.py -l {long_read} " \
              f"-r {reference_fasta} -p {prefix} -o {outdir} -m {mode} -c {config_file}"
    print(command)
    os.system(command)


def config_hybrid(forward_read, reverse_read, long_read,reference_fasta, prefix, outdir, mode, execution_folder, config_file):
    #Config-maker run
    command = f"{execution_folder}/scripts/config-maker.py -1 {forward_read} -2 {reverse_read} " \
              f"-l {long_read} -r {reference_fasta} -p {prefix} -o {outdir} -m {mode} -c {config_file}"
    print(command)
    os.system(command)


def snakerun(snakefile, threads, config_file, debug):

    if debug:
        snake_debug = "-n"
    else:
        snake_debug = ""

    command = f"snakemake --snakefile {snakefile} --configfile {config_file} " \
    f"--cores {threads} --use-conda --conda-frontend mamba {snake_debug}"
    print(command)
    os.system(command)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pannopi - a tool for prokariotic genome assembly and annotation.')
    parser.add_argument('-m','--mode', help="mode to use [default = short]", 
                        choices=["short", "long", "hybrid"], default="short")
    parser.add_argument('-r','--reference', help="path to reference asssembly in FASTA format", required=False, default="0")
    parser.add_argument('-1','--forward_reads', help="path to forward short read file in FASTQ format", default="0")
    parser.add_argument('-2','--reverse_reads', help="path to reverse short read file in FASTQ format", default="0")
    parser.add_argument('-l','--long_reads', help="path to long read file in FASTQ format", default="0")
    parser.add_argument('-p','--prefix', help="prefix for output files", default="0")
    parser.add_argument('-o','--outdir', help='output directory', required=True)
    parser.add_argument('-t','--threads', help='number of threads [default == 8]', default = "8")
    parser.add_argument('-d','--debug', help='debug mode', action='store_true')
    
    args = vars(parser.parse_args())

    reference_fasta = args["reference"]
    forward_read = args["forward_reads"]
    reverse_read = args["reverse_reads"]
    long_read = args["long_reads"]
    prefix = args["prefix"]
    outdir = os.path.abspath(args["outdir"])
    threads = args["threads"]
    debug = args["debug"]
    mode = args["mode"]
    
    execution_folder = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
    execution_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    random_letters = "".join([random.choice(string.ascii_letters) for n in range(3)])
    config_file = os.path.join(execution_folder, f"config/config_{random_letters}{execution_time}.yaml")
    settings_file = os.path.join(execution_folder, "workflows/settings.snakefile")

    if reference_fasta != "0":
        reference_fasta = os.path.abspath(reference_fasta)
    else:
        reference_fasta = False

    if prefix == "0":
        if forward_read != "0":
            prefix = os.path.basename(forward_read).split("_")[0]
        elif long_read != "0":
            prefix = os.path.basename(long_read).split(".")[0]


    if check_for_databases(settings_file):
        # Check that all files required for each mode are in and run pipeline
        if mode == "short":
            if forward_read == "0" or reverse_read == "0":
                parser.error("\nShort-reads mode requires -1 {path_to_forward_read} and -2 {path_to_reverse_read}!")
            elif long_read != "0":
                parser.error("\nShort-reads mode requires -1 {path_to_forward_read} and -2 {path_to_reverse_read} only!\nTo analyse long-reads use long-reads mode or hybrid mode")
            else:
                forward_read = os.path.abspath(forward_read)
                reverse_read = os.path.abspath(reverse_read)
                snakefile = os.path.join(execution_folder, "workflows/short_mode.snakefile")
                config_short(forward_read, reverse_read, reference_fasta, prefix, outdir, mode, execution_folder, config_file)

        elif mode == "long":
            if long_read == "0":
                parser.error("\nLong-read mode requires -l {path_to_long_reads.fq}!")
            elif forward_read != "0" or reverse_read != "0":
                parser.error("\nLong-reads mode requires -l {path_to_long_reads.fq} only!\nTo analyse short-reads use short-reads mode or hybrid mode")
            else:
                long_read = os.path.abspath(long_read)
                snakefile = os.path.join(execution_folder, "workflows/long_mode.snakefile")
                config_long(long_read, reference_fasta, prefix, outdir, mode, execution_folder, config_file)

        elif mode == "hybrid":
            if forward_read == "0" or reverse_read == "0" or long_read == "0":
                parser.error("\nHybrid mode requires -1 {path_to_forward_read} AND -2 {path_to_reverse_read} AND -l {path_to_long_reads.fq}!")
            else:
                long_read = os.path.abspath(long_read)
                forward_read = os.path.abspath(forward_read)
                reverse_read = os.path.abspath(reverse_read)
                snakefile = os.path.join(execution_folder, "workflows/hybrid_mode.snakefile")
                config_hybrid(forward_read, reverse_read, long_read,reference_fasta, prefix, outdir, mode, execution_folder, config_file)

    snakerun(snakefile, threads, config_file, debug)
