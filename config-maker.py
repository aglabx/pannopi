#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 15.05.2021
#@author: Zilov Danil, GitHUB: zilov
#@contact: zilov.d@gamail.com

import argparse
import os
import os.path
from inspect import getsourcefile

def config_universal(prefix, outdir, reference):
    config_uni = f"""
prefix: "{prefix}"    

#ASSEMBLY
assembly_dir: "{outdir}/genome_assembly/unicycler"
assembly: "{outdir}/genome_assembly/unicycler/assembly.fasta"

#ASSEMBLY QUALITY CONTROL
quast_dir: "{outdir}/genome_assembly/QC/quast"
quast_out_file: "{outdir}/genome_assembly/QC/quast/report.txt"

# STRUCTURAL ANNOTATION
# prokka
annotation_dir: "{outdir}/struct_annotation/prokka/"
annotation_faa: "{outdir}/struct_annotation/prokka/{prefix}.faa"
annotation_gbk: "{outdir}/struct_annotation/prokka/{prefix}.gbk"
# busco QC
busco_dir: "{outdir}/struct_annotation/QC/busco"
busco_outfile: "{outdir}/struct_annotation/QC/{prefix}_busco/short_summary.bacteria_odb10.{prefix}_busco.txt"

# FUNCTIONAL ANNOTATION

#eggnog
eggnog_dir: "{outdir}/eggnog/"
eggnog_prefix: "{prefix}"
eggnog_out_annotation: "{outdir}/eggnog/{prefix}.emapper.annotations"
eggnog_out_orthologs: "{outdir}/eggnog/{prefix}.emapper.seed_orthologs"

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
results_file: "{outdir}/results/{prefix}_AMR_and_virulence_summary.txt"
"""
    if reference:
        config_ref = f"""
reference_file: "{reference}"
fastani_dir: "{outdir}/QC/fastani"
fastani_outfile: "{outdir}/QC/fastani/{prefix}_fastani.txt"
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
rmdup_out_file1: "{outdir}/preparation/rmdup/{prefix}.rm_1.fastq"
rmdup_out_file2: "{outdir}/preparation/rmdup/{prefix}.rm_2.fastq"
rmdup_out_statistics: "{outdir}/preparation/rmdup/{prefix}.rm.stats"

#FASTQC
fastqc1_dir: "{outdir}/preparation/QC/fastqc/fastqc_raw"
fastqc2_dir: "{outdir}/preparation/QC/fastqc/fastqc_clean"
fastqc_file1: "{outdir}/preparation/QC/fastqc/fastqc_raw/{prefix}_1_fastqc.zip"
fastqc_file2: "{outdir}/preparation/QC/fastqc/fastqc_clean/{prefix}.rm_2_fastqc.zip"

#JELLY FILES
jellycount_file: "{outdir}/preparation/QC/jellyfish/{prefix}.jf2"
jellyhisto_file: "{outdir}/preparation/QC/jellyfish/{prefix}.histo"
scope_dir: "{outdir}/preparation/QC/jellyfish/scope/"
scope_file: "{outdir}/preparation/QC/jellyfish/scope/plot.png"
"""
    return config_short
    

def config_long_mode(long_read, prefix, outdir):
    config_long = f"""
long_reads_file: {long_read}
"""
    return config_long


def config_hybrid_mode(long_read, forward_read, reverse_read, prefix, outdir):
    config_hybrid = config_short_mode(forward_read, reverse_read, prefix, outdir) + \
                    config_universal(long_read, prefix, outdir)
    return config_hybrid

    

def main(forward_read, reverse_read, long_read, prefix, outdir, mode, execution_folder):
    ''' Function description.
    '''
    config_file = f"{execution_folder}/config/config.yaml"

    
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
    args = vars(parser.parse_args())
    
    # All of parameters goes in absolute paths from pannopi.py
    forward_read = args["forward_read"]
    reverse_read = args["reverse_read"]
    long_read = args["long_read"]
    reference = args["reference"]
    outdir = args["outdir"]
    mode = args["mode"]
    prefix =args["prefix"]
    
    execution_folder = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))

    main(forward_read, reverse_read, long_read, prefix, outdir, mode, execution_folder)
