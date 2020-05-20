#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: <data>
#@author: <name>
#@contact: <email>

import sys
import argparse
import pymongo
import os
import os.path


def main():
    ''' Function description.
    '''
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    ncbi = myclient["NCBI"]
    refids = ncbi.refids
    taxids = ncbi.taxids
    
    cont_to_len = {}
    with open(bact_fai) as fh:
        for line in fh:
            a = line.strip().split("\t")
            cont_to_len[a[0]] = int(a[1])
            
    cont_to_blast = {}
    with open(blast_file) as fh:
        for line in fh:
            a = line.strip().split("\t")
            cont_to_blast[a[0]] = a[1]
    
    from collections import Counter
    count_names = Counter()
    count_id = Counter()
    total_length = 0
    not_bacteria_node = []
    unnown_id = []
    with open(contera_log, "w") as fw:
        fw.write("UNNOWN ID'S: \n")
        for key, value in cont_to_blast.items():
            length = cont_to_len[key]
            val_split = value.split('.')[0]
            taxon_id = refids.find_one({"accession":val_split})
            if taxon_id == None:
                fw.write(key + " : " + val_split + "\n")
            else:
                taxon_id = taxon_id["taxid"]
                taxon_name = taxids.find_one({"_id":taxon_id})["name"]
                taxon_name = " ".join(taxon_name.split()[:2])
                count_names[taxon_name] += length
                count_id[taxon_id] += length
                total_length += length
                if taxon_name != count_names.most_common()[0][0]:
                    not_bacteria_node.append(key)
         
    bact_report = []
    for taxon, size in count_names.most_common(100):
        bact_report.append(taxon + " " + "%s%%" % round(100.*size/total_length, 2))
    print("\n", bact_report, "\n")
        
    bacteria_id = []
    for i in count_id.most_common()[:3]:
        bacteria_id.append(str(i[0]) + " = " + str(i[1]/total_length * 100) + "%")
    print("THE MOST COMMON ID IS : " + ", ".join(bacteria_id))
    
    print("NODES TO BE ERASED:", not_bacteria_node, "\n")
    
    print(len(not_bacteria_node), "NODES WILL BE ERASED!", "\n")
        
    fasta = {}
    header = None
    with open(scaffold) as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if line.startswith(">"):
                if header:
                    fasta[header]="".join(seq)
                header = line
                seq = []
            else:
                seq.append(line)
    if header:
        fasta[header] = "".join(seq)
        
    real_node = []
    for i in not_bacteria_node:
        for key in fasta.keys():
            if key.startswith(">" + i):
                real_node.append(key)
    
    for i in real_node:
        if i in fasta.keys():
            fasta.pop(i)
        
    short_contig = []
    for key, value in fasta.items():
        if len(value) < 200:
            short_contig.append(key)
            
    for i in short_contig:
        if i in fasta.keys():
            fasta.pop(i)
            
    with open(scaffolds_filtered, "w") as fw:
        for key, value in fasta.items():
            fw.write(key + "\n" + value + "\n")
    fw.close()
    
    command = "makeblastdb -in %s -dbtype nucl -parse_seqids" % adapters
    check_file = os.path.exists(settings["fastqc_file"])
    if check_file == True:
        if os.path.getsize(settings["fastqc_file"]) > 0:
            print("U've already done FASTQC")
            pass
        else:
            print(command)
            os.system(command)
    else:
        print(command)
        os.system(command)
    
    with open(contera_report, "w") as fw:
        fw.write("BACTERIAL CONTENT OF READS IS:\n" + ", ".join(bact_report) + "\n\n")
        fw.write("THE MOST COMMON ID IS:\n" + "Taxon IDs: " + ", ".join(bacteria_id) + "\n\n")
        fw.write("NODES TO BE ERASED:\n" + ", ".join(not_bacteria_node) + "\n\n")
        fw.write(str(len(not_bacteria_node)) + " NODES WERE ERASED!\n\n")
        fw.write("Scaffolds without contamination lays in " + scaffold.replace(".fasta", "_filtered.fasta"))
    fw.close()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Bacterial genome contamination erasing tool')
    parser.add_argument('-s','--scaffold', help='whole path to scaffold_file', required=True)
    parser.add_argument('-f','--fai', help='whole path to fai_file', required=True)
    parser.add_argument('-b','--blastn', help='whole path to best_single_hits.blastn', required=True)
    parser.add_argument('-a','--adapters', help='whole path to adapters database in fasta format', required=True)
    parser.add_argument('-o','--output', help='output_path', required=True)
    args = vars(parser.parse_args())
    
    scaffold = args["scaffold"]
    bact_fai = args["fai"]
    blast_file = args["blastn"]
    adapters = args["adapters"]
    output = args["output"]
    scaforarg = scaffold.split("/")[-1].split(".")[0]
    prefix = blast_file.split("/")[-1].split(".")[0]
    
    scaffolds_filtered = output + scaforarg + "_filtered.fasta"
    contera_report = output + prefix + ".contera_report.txt"
    contera_log = output + prefix + ".contera.log"
    adapters_report = output + prefix + ".adapters_report.outfmt6"
    
    main()
