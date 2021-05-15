#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: <data>
#@author: <name>
#@contact: <email>

import argparse
import os
import os.path
from inspect import getsourcefile


def main():
    ''' Function description.
    '''
    pass


    
    if test:
        workdir = "test_data/"
    else:
        workdir = "data/"
        
    if debug:
        snake_debug = "-n"
    else:
        snake_debug = ""

    workdir_list = []
    for i in os.listdir(workdir):
        if i.startswith("."):
            continue
        else:
            if os.path.isdir(workdir + i) == True:
                workdir_list.append(os.path.abspath(workdir + i))

    for workdir in workdir_list:
        #Reads prepare
        command = "python tools/reads_prepare/reads_prepare.py -w %s" % workdir
        os.system(command)
        #Config-maker
        command = "python config-maker.py -w %s -a %s -n %s" % (workdir, assembler, annotator)
        print(command)
        os.system(command)
        #Snakemake
        command = "snakemake --cores %s --use-conda %s" % (cpus, snake_debug)
        print(command)
        os.system(command)
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pannopi - a tool for prokariotic genome assembly and annotation.')
    parser.add_argument('-m','--mode', help="mode to use [default = short]", 
                        choices=["short", "long", "hybrid"], default="short")
    parser.add_argument('-r','--reference', help="path to reference asssembly in FASTA format", required=False. default="0")
    parser.add_argument('-1','--forward_reads', help="path to forward short read file in FASTQ format", default="0")
    parser.add_argument('-2','--reverse_reads', help="path to reverse short read file in FASTQ format", default="0")
    parser.add_argument('-l','--long_reads', help="path to long read file in FASTQ format", default="0")
    parser.add_argument('-o','--outdir', help='output directory', required=True)
    parser.add_argument('-t','--threads', help='number of threads [default == 8]', default = "8")
    parser.add_argument('-d','--debug', help='debug mode', action='store_true')
    args = vars(parser.parse_args())

    reference_fasta = args["reference"]
    threads = args["threads"]
    debug = args["debug"]
    mode = args["mode"]
    forward_read = args["forward_reads"]
    reverse_read = args["reverse_reads"]
    long_read = args["long_reads"]
    outdir = os.path.abspath(args["outdir"])
    
    execution_folder = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
        
        
    # Check that all files required for each mode are in    
    if mode == "short":
        if forward_read == "0" or reverse_read == "0":
            parser.error("\nShort-reads mode requires -1 {path_to_forward_read} and -2 {path_to_reverse_read}!")
        elif long_read != "0":
            parser.error("\nShort-reads mode requires -1 {path_to_forward_read} and -2 {path_to_reverse_read} only!\
             To analyse long-reads use long-reads mode or hybrid mode")
        else:
            forward_read = os.path.abspath(forward_read)
            reverse_read = os.path.abspath(reverse_read)
            
    elif mode == "long":
        if long_read == "0":
            parser.error("\nLong-read mode requires -l {path_to_long_reads.fq}!")
        elif forward_read != "0" or reverse_read != "0":
            parser.error("\nLong-reads mode requires -l {path_to_long_reads.fq} only!\ 
            To analyse short-reads use short-reads mode or hybrid mode")
        else:
            long_read = os.path.abspath(long_read)
            
    elif mode == "fasta_rna_faa":
        if forward_rna_read == "0" or reverse_rna_read == "0" or faa_file == "0":
            parser.error("\nHybrid mode requires -1 {path_to_forward_read} AND -2 {path_to_reverse_read} AND -l {path_to_long_reads.fq}!")
        else:
            faa_file = os.path.abspath(faa_file)
            forward_rna_read = os.path.abspath(forward_rna_read)
            reverse_rna_read = os.path.abspath(reverse_rna_read)
            
    if reference_fasta != "0":
        reference_fasta = os.path.abspath(reference_fasta)
    else:
        reference_fasta = False
    main(reference_fasta, forward_read, reverse_read, long_read, outdir, threads, mode, execution_folder, debug)