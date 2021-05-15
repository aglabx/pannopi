#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 15.05.2021
#@author: Zilov Danil, GitHUB: zilov
#@contact: zilov.d@gamail.com

import argparse
import os
import os.path


def main(forward_read, reverse_read, long_read, prefix, outdir, mode):
    ''' Function description.
    '''
    pass
    execution_folder = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
    config_file = f"{execution_folder}/config/config.yaml"
    
    config_parameters = f"""
# MAIN PARAMETERS

# databases
eggnog_db: "/mnt/projects/databases/eggnog_db/"
blast_nt_db: ""
    """
    
    config_universal = f"""
    
# ASSEMBLY

#ASSEMBLY
assembly_dir: "{outdir}/genome_assembly/unicycler"
assembly: "{outdir}/genome_assembly/unicycler/assembly.fasta"

# FILTERING
adapters_fasta: "tools/contera/adapters_db/adaptor_fasta.fna"
assembly_filtered: "{outdir}/genome_assembly/QC/contera/scaffolds_filtered.fasta"
contera_dir:  "{outdir}/genome_assembly/QC/contera/"
contera_report: "{outdir}/genome_assembly/QC/contera/{prefix}.contera_report.txt"
adapters_report: "{outdir}/genome_assembly/QC/contera/{prefix}.adapters_report.outfmt6"

#ASSEMBLY QUALITY CONTROL
quast_dir: "{outdir}/genome_assembly/QC/quast"
quast_out_file: "{outdir}/genome_assembly/QC/quast/report.txt"

# STRUCTURAL ANNOTATION
# prokka
annotation_dir: "{outdir}/struct_annotation/{annotator}/"
annotation_faa: "{outdir}/struct_annotation/{annotator}/{prefix}.faa"
annotation_gbk: "{outdir}/struct_annotation/{annotator}/{prefix}.gbk"


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
funcan_sum: "{outdir}/func_annotation/{prefix}_AMR_and_virulence_report.txt"
mlst: "{outdir}/func_annotation/{prefix}_mlst_type.txt"

#RESULT STEP
results_path: "{outdir}/results/"
    """
    
    if forward_read:
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
        
    if long_read:
        config_long = f"""
        long_reads_file = {long_read}
        """
            
    
    if mode == "short":
        unicycler_rule = os.path.join(execution_folder,"rules/unicycler_short.smk")
        config = config_paremeters + config_short + config_universal
    elif mode == "long":
        unicucler_rule = os.path.join(execution_folder,"rules/unicycler_long.smk")
        config = config_parameters + config_long + config_universal
    elif mode == "hybrid":
        unicycler_rule = os.path.join(execution_folder,"rules/unicycler_hybrid.smk") 
        config = config_parameters + config_short + config_long + config_universal
    
    
    with open(config_file, "w") as fw:
        fw.write(config)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('-1', '--forward_read', help='sample directory', required=False, default=False)
    parser.add_argument('-2', '--reverse_read', help='sample directory', required=False, default=False)
    parser.add_argument('-l', '--long_read', help='sample directory', required=False, default=False)
    parser.add_argument('-m', '--mode', help = 'Pannopi mode', required = True)
    parser.add_argument('-p', '--prefix', help='Prefix for output files', required=True)
    parser.add_argument('-o', '--outdir', help='Output directory', required=True)
    args = vars(parser.parse_args())
    
    # All of parameters goes in absolute paths from pannopi.py
    forward_read = args["forward_read"]
    reverse_read = args["reverse_read"]
    long_read = args["long_read"]
    outdir = args["outdir"]
    mode = args["mode"]
    prefix =args["prefix"]

    main(forward_read, reverse_read, long_read, prefix, outdir, mode)