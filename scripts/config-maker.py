#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 15.05.2021
#@author: Zilov Danil, GitHUB: zilov
#@contact: zilov.d@gamail.com

import argparse

def config_universal(prefix, outdir, reference):
    config_uni = f"""
prefix: "{prefix}"    

#ASSEMBLY
assembly_dir: "{outdir}/genome_assembly/unicycler"
assembly: "{outdir}/genome_assembly/unicycler/assembly.fasta"
contera_dir: "{outdir}/genome_assembly/contera"
contera_out_file: "{outdir}/genome_assembly/contera/assembly_filtered.fasta"

#ASSEMBLY QUALITY CONTROL
quast_dir: "{outdir}/genome_assembly/QC/quast"
quast_out_file: "{outdir}/genome_assembly/QC/quast/report.txt"

# STRUCTURAL ANNOTATION
# prokka
annotation_dir: "{outdir}/struct_annotation/prokka/"
annotation_faa: "{outdir}/struct_annotation/prokka/{prefix}.faa"
annotation_gbk: "{outdir}/struct_annotation/prokka/{prefix}.gbk"
# busco QC
busco_run_dir: "{outdir}/struct_annotation/QC"
busco_summary: "{outdir}/struct_annotation/QC/busco/short_summary.specific*.txt"
busco_outfile: "{outdir}/struct_annotation/QC/busco/{prefix}_busco.txt"

# FUNCTIONAL ANNOTATION

#eggnog
eggnog_dir: "{outdir}/func_annotation/eggnog/"
eggnog_prefix: "{prefix}"
eggnog_out_annotation: "{outdir}/func_annotation/eggnog/{prefix}.emapper.annotations"
eggnog_out_orthologs: "{outdir}/func_annotation/eggnog/{prefix}.emapper.seed_orthologs"

funcan_dir: "{outdir}/func_annotation/"
megares: "{outdir}/func_annotation/{prefix}_megares_report.txt"
ncbi: "{outdir}/func_annotation/{prefix}_ncbi_report.txt"
virulence: "{outdir}/func_annotation/{prefix}_virulence_report.txt"
plasmids: "{outdir}/func_annotation/{prefix}_plasmids_report.txt"
serotype: "{outdir}/func_annotation/{prefix}_serotype_ecoli.txt"
abricate_summary: "{outdir}/func_annotation/{prefix}_AMR_and_virulence_summary.txt"
mlst: "{outdir}/func_annotation/{prefix}_mlst_type.txt"

#RESULT STEP
results_path: "{outdir}/results/"
results_file: "{outdir}/results/{prefix}_fastani.txt"

#logs_and_benchmarks

pannopi_log: "{outdir}/logs/pannopi.log"
v2trim_log: "{outdir}/logs/v2trim.log"
rmdup_log: "{outdir}/logs/rmdup.log"
genomescope_log: "{outdir}/logs/genomescope.log"
unicycler_log: "{outdir}/logs/unicycler.log"
prokka_log: "{outdir}/logs/prokka.log"
fastani_log: "{outdir}/logs/fastani.log"
busco_log: "{outdir}/logs/busco.log"
eggnog_log: "{outdir}/logs/eggnog.log"

pannopi_bench: "{outdir}/benchmark/pannopi.tsv"
pannopi_bench: "{outdir}/benchmark/pannopi.tsv"
v2trim_bench: "{outdir}/benchmark/v2trim.tsv"
rmdup_bench: "{outdir}/benchmark/rmdup.tsv"
genomescope_bench: "{outdir}/benchmark/genomescope.tsv"
unicycler_bench: "{outdir}/benchmark/unicycler.tsv"
prokka_bench: "{outdir}/benchmark/prokka.tsv"
fastani_bench: "{outdir}/benchmark/fastani.tsv"
busco_bench: "{outdir}/benchmark/busco.tsv"
eggnog_bench: "{outdir}/benchmark/eggnog.tsv"

"""
    if reference:
        config_ref = f"""
reference_file: "{reference}"
fastani_dir: "{outdir}/structural_annotation/QC/fastani"
fastani_outfile: "{outdir}/structural_annotation/QC/fastani/{prefix}_fastani.txt"
"""
    else:
        config_ref = """
reference_file: "0"
        """

    config_uni += config_ref
    return config_uni

def config_short_mode(forward_read, reverse_read, prefix, outdir):
    config_short = f"""

# PREPARATION 

#v2trim
v2trim_dir: "{outdir}/preparation/v2trim/"
v2trim_in_file1: "{forward_read}"
v2trim_in_file2: "{reverse_read}"
v2trim_prefix: "{prefix}"
v2trim_out_file1: "{outdir}/preparation/v2trim/{prefix}.trim_1.fastq"
v2trim_out_file2: "{outdir}/preparation/v2trim/{prefix}.trim_2.fastq"
v2trim_out_statistics: "{outdir}/preparation/v2trim/{prefix}.stats"

#rmdup
rmdup_dir: "{outdir}/preparation/rmdup/"
rmdup_prefix: "{outdir}/preparation/rmdup/{prefix}.rm"
rmdup_out_file1: "{outdir}/preparation/rmdup/{prefix}.rm_1.fastq"
rmdup_out_file2: "{outdir}/preparation/rmdup/{prefix}.rm_2.fastq"
rmdup_out_statistics: "{outdir}/preparation/rmdup/{prefix}.rm.stats"

#FASTQC
fastqc1_dir: "{outdir}/preparation/QC/fastqc_raw"
fastqc2_dir: "{outdir}/preparation/QC/fastqc_clean"
fastqc_file1: "{outdir}/preparation/QC/fastqc_raw/{prefix}_1_fastqc.zip"
fastqc_file2: "{outdir}/preparation/QC/fastqc_clean/{prefix}.trim_2_fastqc.zip"

#JELLY FILES
jellycount_file: "{outdir}/preparation/QC/jellyfish/{prefix}.jf2"
jellyhisto_file: "{outdir}/preparation/QC/jellyfish/{prefix}.histo"
scope_dir: "{outdir}/preparation/QC/genomescope/"
scope_file: "{outdir}/preparation/QC/genomescope/{prefix}_linear_plot.png"
"""
    return config_short
    

def config_long_mode(long_read, prefix, outdir):
    config_long = f"""
long_reads_file: "{long_read}"
"""
    return config_long


def config_hybrid_mode(long_read, forward_read, reverse_read, prefix, outdir):
    config_hybrid = config_short_mode(forward_read, reverse_read, prefix, outdir) + \
                    config_long_mode(long_read, prefix, outdir)
    return config_hybrid

    

def main(forward_read, reverse_read, long_read, prefix, outdir, mode, config_file):
    
    if mode == "short":
        config = config_short_mode(forward_read, reverse_read, prefix, outdir) + \
                 config_universal(prefix, outdir, reference)
    elif mode == "long":
        config = config_long_mode(long_read, prefix, outdir) + config_universal(prefix, outdir, reference)
    elif mode == "hybrid":
        config = config_hybrid_mode(long_read, forward_read, reverse_read, prefix, outdir) + \
                 config_universal(prefix, outdir, reference)
    
    
    with open(config_file, "w") as fw:
        fw.write(config)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('-1', '--forward_read', help='sample directory', required=False, default=False)
    parser.add_argument('-2', '--reverse_read', help='sample directory', required=False, default=False)
    parser.add_argument('-l', '--long_read', help='sample directory', required=False, default=False)
    parser.add_argument('-r', '--reference', help='path to reference file', required=False, default=False)
    parser.add_argument('-m', '--mode', help = 'Pannopi mode', required = True)
    parser.add_argument('-p', '--prefix', help='Prefix for output files', required=True)
    parser.add_argument('-o', '--outdir', help='Output directory', required=True)
    parser.add_argument('-c', '--configfile', help='path_to_configfile', required=True)
    args = vars(parser.parse_args())
    
    # All of parameters goes in absolute paths from pannopi.py
    forward_read = args["forward_read"]
    reverse_read = args["reverse_read"]
    long_read = args["long_read"]
    reference = args["reference"]
    outdir = args["outdir"]
    mode = args["mode"]
    prefix =args["prefix"]
    config_file = args["configfile"]

    main(forward_read, reverse_read, long_read, prefix, outdir, mode, config_file)
