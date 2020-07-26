#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: <data>
#@author: <name>
#@contact: <email>

import sys
import argparse


def main():
    ''' Function description.
    '''
    pass

    import os
    import os.path

    config_file = "config/config.yaml"

    for i in os.listdir(work_dir):
        if i.endswith(".fastq"):
            prefix = "_".join(i.split("_")[:-1])
    path_to_reads = os.path.abspath(work_dir)
    for i in os.listdir(work_dir):
        if i.endswith("_1.fastq"):
            raw_fastq_1 = path_to_reads + "/" + i
            print(raw_fastq_1)
        elif i.endswith("_2.fastq"):
            raw_fastq_2 = path_to_reads + "/" + i
            print(raw_fastq_2)

    if assembler == "spades":
        assembly_file = "scaffolds"
        assembly_gfa = "assembly_graph_with_scaffolds.gfa"
    elif assembler == "unicycler":
        assembly_file = "assembly"
    elif assembler == "skesa":
        assembly_file = "??????????????" ##### УЗНАТЬ НАПИСАТЬ ДОПОЛНИТЬ

    config = """
assembler: "rules/{assembler}.sf"
annotator: "rules/{annotator}.sf"
raw_fastq_1: "{raw_fastq_1}"
raw_fastq_2: "{raw_fastq_2}"
path_to_reads: "{path_to_reads}"
prefix: "{prefix}"

#PREPARE
trim_in_prefix: "{path_to_reads}/{prefix}"
trim_out_prefix: "{path_to_reads}/preparation/trim/{prefix}"
rmdub_in_prefix: "{path_to_reads}/preparation/trim/{prefix}.trim"
rmdub_out_prefix: "{path_to_reads}/preparation/rmdub/{prefix}.rm"
trim_out_file_1:  "{path_to_reads}/preparation/trim/{prefix}.trim_1.fastq"
trim_out_file_2: "{path_to_reads}/preparation/trim/{prefix}.trim_2.fastq"
rmdub_file_1: "{path_to_reads}/preparation/rmdub/{prefix}.rm_1.fastq"
rmdub_file_2: "{path_to_reads}/preparation/rmdub/{prefix}.rm_2.fastq"

#FASTQC
fastqc1_dir: "{path_to_reads}/preparation/QC/fastqc/fastqc_raw"
fastqc2_dir: "{path_to_reads}/preparation/QC/fastqc/fastqc_clean"
fastqc_file1: "{path_to_reads}/preparation/QC/fastqc/fastqc_raw/{prefix}_1_fastqc.zip"
fastqc_file2: "{path_to_reads}/preparation/QC/fastqc/fastqc_clean/{prefix}.rm_2_fastqc.zip"

#JELLY FILES
jellycount_file: "{path_to_reads}/preparation/QC/jellyfish/{prefix}.jf2"
jellyhisto_file: "{path_to_reads}/preparation/QC/jellyfish/{prefix}.histo"
scope_dir: "{path_to_reads}/preparation/QC/jellyfish/scope/"
scope_file: "{path_to_reads}/preparation/QC/jellyfish/scope/plot.png"

#ASSEMBLY
assembly: "{path_to_reads}/genome_assembly/{assembler}/{assembly_file}.fasta"
assembly_dir: "{path_to_reads}/genome_assembly/{assembler}"
assembly_gfa: "{path_to_reads}/genome_assembly/{assembler}/{assembly_gfa}"

#ASSEMBLY QUALITY CONTROL
quast_dir: "{path_to_reads}/genome_assembly/QC/quast"
quast_out_file: "{path_to_reads}/genome_assembly/QC/quast/report.txt"
reference_dir: "{path_to_reads}/genome_assembly/QC/contera/reference/"
reference_file: "{path_to_reads}/reference/{prefix}.fna"

#BLAST
blastn_out: "{path_to_reads}/genome_assembly/QC/blast/{prefix}.outfmt6"
blast_db: "nt"

# FILTERING
adapters_fasta: "tools/contera/adapters_db/adaptor_fasta.fna"
assembly_filtered: "{path_to_reads}/genome_assembly/QC/contera/scaffolds_filtered.fasta"
contera_dir:  "{path_to_reads}/genome_assembly/QC/contera/"
contera_report: "{path_to_reads}/genome_assembly/QC/contera/{prefix}.contera_report.txt"
adapters_report: "{path_to_reads}/genome_assembly/QC/contera/{prefix}.adapters_report.outfmt6"

# STRUCTURAL ANNOTATION
annotation_dir: "{path_to_reads}/struct_annotation/{annotator}/"
annotation_faa: "{path_to_reads}/struct_annotation/{annotator}/{prefix}.faa"
annotation_gbk: "{path_to_reads}/struct_annotation/{annotator}/{prefix}.gbk"

# FUNCTIONAL ANNOTATION
eggnog_dir: "{path_to_reads}/func_annotation/eggnog"
eggnog_ann: "{path_to_reads}/func_annotation/eggnog/{prefix}.emapper.annotations"
goann_outdir: "{path_to_reads}/func_annotation/goann/"
goann_out: "{path_to_reads}/func_annotation/goann/{prefix}_genes_analysis.txt"
funcan_dir: "{path_to_reads}/func_annotation/"
megares: "{path_to_reads}/func_annotation/megares_report.txt"
ncbi: "{path_to_reads}/func_annotation/ncbi_report.txt"
virulence: "{path_to_reads}/func_annotation/virulence_report.txt"
plasmids: "{path_to_reads}/func_annotation/plasmids_report.txt"
serotype: "{path_to_reads}/func_annotation/serotype_ecoli.txt"
funcan_sum: "{path_to_reads}/func_annotation/AMR_and_virulence_report.txt"
mlst: "{path_to_reads}/func_annotation/mlst_type.txt"

#RESULT STEP
results_path: "{path_to_reads}/results/"
results_file: "{path_to_reads}/results/{prefix}_genes_analysis.txt"
    """.format(path_to_reads = path_to_reads, prefix = prefix,\
    assembly_file = assembly_file, assembly_gfa = assembly_gfa, assembler = assembler, annotator = annotator, raw_fastq_1 = raw_fastq_1,\
    raw_fastq_2 = raw_fastq_2)

    with open(config_file, "w") as fw:
        fw.write(config)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('-w', '--workdir', help='sample directory', required=True)
    parser.add_argument('-a', '--assembler', help='assebler tool: spades unicycler or skesa', required=True)
    parser.add_argument('-n', '--annotator', help='annotation tool: pgap or prokka', required=True)
    args = vars(parser.parse_args())

    work_dir = args["workdir"]
    assembler = args["assembler"]
    annotator = args["annotator"]

    main()
