#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 15.05.2021
# @author: Zilov Danil, GitHUB: zilov
# @contact: zilov.d@gamail.com

import argparse
import glob
import os

def quast_report(quast_file):
    quast_report = {}
    with open(quast_file) as fh:
        for line in fh:
            line = line.strip().split("\t")
            if line[0] == "# contigs":
                contigs_n = line[1]
                quast_report["Contigs_number"] = contigs_n
            elif line[0] == "Total length (>= 0 bp)":
                length = line[1]
                quast_report["Total_length"] = length
            elif line[0] == "N50":
                n50 = line[1]
                quast_report["N50"] = n50
            elif line[0] == "# misassemblies":
                misasemblies = line[1]
                quast_report["Misassemblies"] = misasemblies
            elif line[0] == "Genome fraction (%)":
                genome_fraction = line[1]
                quast_report["Genome_fraction"] = genome_fraction
    return quast_report

def prokka_report(prokka_file):
    prokka_report = {}
    with open(prokka_file) as fh:
        for line in fh:
            line = line.strip().split(": ")
            if line[0] == "CDS":
                cds = line[1]
                prokka_report["CDS"] = cds
            elif line[0] == "rRNA":
                rrna = line[1]
                prokka_report["rRNA"] = rrna
            elif line[0] == "tRNA":
                trna = line[1]
                prokka_report["tRNA"] = trna
    return prokka_report


def fastani_report(fastani_file):
    fastani_report = {}
    with open(fastani_file) as fh:
        for line in fh:
            line = line.strip().split("\t")
            fastani_report["FastANI"] = line[-3]
            return fastani_report

def busco_report(busco_dir):
    busco_files = glob.glob(os.path.join(busco_dir, "*busco.txt"))
    busco_report = {}
    for file in busco_files:
        with open(file) as fh:
            for line in fh:
                if line.startswith("# The lineage dataset is:"):
                    dataset = "busco_" + line.strip().split()[5]
                line = line.strip()
                if line.startswith("C:"):
                    buscos = line.strip().split("%")[0].split(":")[1]
        busco_report[dataset] = buscos
    return busco_report

def eggnog_report(eggnog_file):
    # eggnog_counter
    eggnog_report = {"Unique_GOs": 0, "Unique_KEGGs": 0}
    with open(eggnog_file) as fh:
        go_list = []
        kegg_ko_list = []
        for line in fh:
            if line.startswith("#"):
                continue
            line = line.strip().split("\t")
            go = line[9]
            if go != "-":
                match_gos_list = go.split(",")
                for match in match_gos_list:
                    if match not in go_list:
                        go_list.append(match)
            kegg_ko = line[11]
            if kegg_ko != "-":
                match_kos_list = kegg_ko.split(",")
                for match in match_kos_list:
                    if match not in kegg_ko_list:
                        kegg_ko_list.append(match)

        eggnog_report["Unique_GOs"] += len(go_list)
        eggnog_report["Unique_KEGGs"] += len(kegg_ko_list)
    return eggnog_report


def abricate_summary(ncbi_file, megares_file, virulence_file, plasmods_file):
    genes = {"NCBI_AMR" : 0, "MEGARES_AMR" : 0, "Virulence_genes" : 0, "Plasmids": 0}
    files = [ncbi_file, megares_file, virulence_file, plasmods_file]
    for file in files:
        file_basename = os.path.basename(file)
        if "ncbi" in file_basename:
            key = "NCBI_AMR"
        elif "megares" in file_basename:
            key = "MEGARES_AMR"
        elif "virulence" in file_basename:
            key = "Virulence_genes"
        elif "plasmids" in file_basename:
            key = "Plasmids"
        with open(file) as fh:
            for line in fh:
                if not line.startswith("#"):
                    genes[key] += 1

    return genes


def pannopi_report(quast_out, prokka_out, fastani_out, busco_out, eggnog_out, ncbi_out,
                   megares_out, virulence_out, plasmids_out, report_file):
    with open(report_file, "w") as fw:
        for stat, value in quast_report(quast_out).items():
            fw.write(f"{stat}\t{value}\n")
        for stat, value in prokka_report(prokka_out).items():
            fw.write(f"{stat}\t{value}\n")
        if fastani_out:
            for stat, value in fastani_report(fastani_out).items():
                fw.write(f"{stat}\t{value}\n")
        busco_dir = os.path.dirname(busco_out)
        for stat, value in busco_report(busco_dir).items():
            fw.write(f"{stat}\t{value}\n")
        for stat, value in eggnog_report(eggnog_out).items():
            fw.write(f"{stat}\t{value}\n")
        for stat, value in abricate_summary(ncbi_out, megares_out, virulence_out, plasmids_out).items():
            fw.write(f"{stat}\t{value}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Config creater for Pannopi pipeline')
    parser.add_argument('-q', '--quast_out_file', help='quast report file', required=True)
    parser.add_argument('-p', '--prokka_out_file', help='prokka report file', required=True)
    parser.add_argument('-b', '--busco_out_file', help='fastani report file', required=True)
    parser.add_argument('-f', '--fastani_out_file', help='fastani report file', required=False, default=False)
    parser.add_argument('-e', '--eggnog_out_file', help='eggnog report file', required=True)
    parser.add_argument('-n', '--ncbi_amr_out', help='abricate ncbi report file', required=True)
    parser.add_argument('-m', '--megares_amr_file', help='abricate megares report file', required=True)
    parser.add_argument('-v', '--virulence_out_file', help='abricate virulence report file', required=True)
    parser.add_argument('-pl', '--plasmids_out_file', help='abricate plasmids report file', required=True)
    parser.add_argument('-o', '--pannopi_out_file', help='pannopi report file', required=True)
    args = vars(parser.parse_args())

    # All of parameters goes in absolute paths from pannopi.py
    quast = args["quast_out_file"]
    prokka = args["prokka_out_file"]
    busco = args["busco_out_file"]
    fastani = args["fastani_out_file"]
    eggnog = args["eggnog_out_file"]
    ncbi = args["ncbi_amr_out"]
    megares = args["megares_amr_file"]
    virulence = args["virulence_out_file"]
    plasmids = args["plasmids_out_file"]
    pannopi_summary = args["pannopi_out_file"]

    res_dir = os.path.dirname(pannopi_summary)
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)

    pannopi_report(quast, prokka, fastani, busco, eggnog, ncbi, megares, virulence, plasmids, pannopi_summary)
    print("Pannopi is done!")
