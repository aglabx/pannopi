#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: <data>
#@author: <name>
#@contact: <email>

import sys
import argparse


def main(settings):
    ''' Function description.
    '''
    pass

    import os
    import os.path

    config_file = "config/config.yaml"

    prefix = "_".join(os.listdir(settings["work_dir"][0].split("_")[:-1])
    path_to_reads = os.path.abspath(work_dir)
    if assembler == "spades":
        assembly_file = "scaffolds"
    elif assembler == "unicycler":
        assembly_file = "assembly"
    elif assembler == "skesa":
        assembly_file = "??????????????" ##### УЗНАТЬ НАПИСАТЬ ДОПОЛНИТЬ

    config = """
    assembler = "rules/{assembler}.sf"
    annotator = "rules/{annotator}.sf"
    raw_fastq_1 : "{raw_fastq_1}"
    raw_fastq_2 : "{raw_fastq_2}"
    path_to_reads : "{path_to_reads}"
    prefix : "{prefix}"

    #PREPARE
    trim_out_file_1 :  "{path_to_reads}/trim/{prefix}.trim_1.fastq",
    trim_out_file_2 : "{path_to_reads}/trim/{prefix}.trim_2.fastq",
    rmdub_file_1 : "{path_to_reads}/rmdub/{prefix}.rm_1.fastq",
    rmdub_file_2 : "{path_to_reads}/rmdub/{prefix}.rm_2.fastq",

    #FASTQC
    fastqc1_dir : "{path_to_reads}/fastqc/fastqc_raw",
    fastqc2_dir : "{path_to_reads}/fastqc/fastqc_clean",
    fastqc_file1 : "{path_to_reads}/fastqc/fastqc_raw/{prefix}_1_fastqc.zip",
    fastqc_file2 : "{path_to_reads}/fastqc/fastqc_clean/{prefix}.rm_2_fastqc.zip",

    #JELLY FILES
    jellycount_file : "{path_to_reads}/jellyfish/{prefix}.jf2",
    jellyhisto_file : "{path_to_reads}/jellyfish/{prefix}.histo",
    scope_dir : "{path_to_reads}/jellyfish/scope/",
    scope_file : "{path_to_reads}/jellyfish/scope/plot.png",

    #ASSEMBLY
    assembly : "{path_to_reads}/assembly/{assembly_file}.fasta",
    assembly_dir : "{path_to_reads}/assembly",
    assembly_gfa : "{path_to_reads}/assembly/{assembly_file}.gfa",

    #QUALITY CONTROL
    quast_dir : "{path_to_reads}/quast",
    quast_out_file : "{path_to_reads}/quast/report.txt",
    reference_dir : "{path_to_reads}/reference/",
    reference_file : "{path_to_reads}/reference/{prefix}.fna",

    #BLAST
    blastn_out : "{path_to_reads}/blast/{prefix}.outfmt6",

    # FILTERING
    filter_out : "{path_to_reads}/blast/{prefix}.best_single_hits.blastn",
    index_file :  "{path_to_reads}/assembly.fasta.fai",
    adapters_fasta : "
    assembly_filtered : "{path_to_reads}/contera/assembly_filtered.fasta",
    contera_dir :  "{path_to_reads}/contera/",
    contera_report : "{path_to_reads}/contera/{prefix}.contera_report.txt",

    # ANNOTATION
    annotation_dir : "{path_to_reads}/annotation/",
    annotation_faa : "{path_to_reads}/annotation/{prefix}.faa",
    annotation_gbk : "{path_to_reads}/annotation/{prefix}.gbk",

    # FUNCTIONAL ANNOTATION
    eggnog_dir : "{path_to_reads}/eggnog/",
    eggnog_ann : "{path_to_reads}/eggnog/{prefix}.emapper.annotations",
    goann_outdir : "{path_to_reads}/goann/",
    goann_out : "{path_to_reads}/goann/{prefix}_genes_analysis.txt",
    funcan_dir : "{path_to_reads}/funcan/",
    megares : "{path_to_reads}/funcan/megares_report.txt",
    ncbi : "{path_to_reads}/funcan/ncbi_report.txt",
    virulence : "{path_to_reads}/funcan/virulence_report.txt",
    plasmids : "{path_to_reads}/funcan/plasmids_report.txt",
    serotype : "{path_to_reads}/funcan/serotype_ecoli.txt",
    funcan_sum : "{path_to_reads}/funcan/AMR_and_virulence_report.txt",
    mlst : "{path_to_reads}/funcan/mlst_type.txt",

    #RESULT STEP
    results_path : "{path_to_reads}/results/",
    results_file : "{path_to_reads}/results/{prefix}_genes_analysis.txt",
    """.format(path_to_reads = path_to_reads, prefix = prefix,\
    assembly_file = assembly_file, raw_fastq_1 = raw_fastq_1,\
    raw_fastq_2 = raw_fastq_2)

    with open(config_file, "w") as fw:
    fw.write(config)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('-w','--workdir', help='sample directory', required=True)
    parser.add_argument('-a','--assembler', help='assebler tool: spades, unicycler or skesa', required=True)
    parser.add_argument('-n','--annotator', help='annotation tool: pgap or prokka', required=True)
    args = vars(parser.parse_args())

    work_dir = args["workdir"]
    assembler = args["assembler"]
    annotator = args["annotator"]

    settings = {
        "work_dir": work_dir,
        "assembler": assembler,
        "annotator" : annotator
    }

    main(settings)
