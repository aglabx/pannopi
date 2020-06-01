#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: <data>
#@author: <name>
#@contact: <email>

import sys
import os
import argparse
import pymongo
from collections import Counter


def main():
    ''' Function description.
    '''
    #SEARCH WORDS, HERE U CAN ADD YOUR ONES
    #OUTPUT_FILES
    anno_tsv = output +  prefix + "_anno.tsv"
    gene_copy_file = output + prefix + "_gene_copy.tsv"
    genes_analysis = output + prefix + "_genes_analysis.txt"
    all_genes_file = output + prefix + "_genes.txt"
    
    dict_GO = {}
    header = None
    with open (obo) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('id: GO') and header == None:
                header = line.replace('id: ', '')
                seq = []
                continue
            elif line.startswith('id: GO') and header != None:
                dict_GO[header] = " ".join(seq[:-2]).lower()
                header = line.replace('id: ', '')
                seq = []
            elif line.startswith("[Typedef]"):
                dict_GO[header] = " ".join(seq[:-2]).lower()
                break
            elif header != None:
                seq.append(line)
    
    from collections import defaultdict
    go2genes = defaultdict(list)
    with open(anno_tsv, "w") as fa:
        with open(egg_anno) as fh:
            for line in fh:
                if line.startswith("#"):
                    continue
                line = line.strip().split("\t")  
                gene_name = line[4]
                GO = line[5].split(",")
                for go in GO:
                    if go in dict_GO:
                        if not line[4]:
                            line[4] = "NA"
                        gene_name = "%s:%s" % (line[0], line[4])
                        go2genes[go].append(gene_name)
        fh.close()
        for go in go2genes.keys():
            fa.write("%s\t%s\t%s\n" % (go, ",".join(list(set(go2genes[go]))), dict_GO[go]))
    fa.close()
            
    gene_copy = defaultdict(int)
    with open(egg_anno) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            line = line.strip().split("\t")  
            if not line[4]:
                line[4] = "NA"
            else:
                gene_copy[line[4]] += 1
    fh.close()

    with open(gene_copy_file, "w") as fw:
        for gene_name, copy_number in gene_copy.items():
            fw.write("%s\t%s\n" % (gene_name, copy_number))
    fw.close()

    command = "less "  + egg_anno  + " | cut -f 5 > " + all_genes_file
    os.system(command)
    
    interest_gene_dict  = {}
    unique_genes_dict = {}
    search_words = ["invasion", "adhesion", "o antigen", "h antigen", "toxin metabol"]
    for word in search_words:
        genes_list = []
        unique_genes = []
        report = []
        with open(anno_tsv) as f:

            #ADDING ALL LINES WITH A WORD INTO THE LIST
            for line in f:
                if word in line:
                    genes_list.append(line)

        #ERASE ALL USELESS INFORMATION
        for i in genes_list:
            report_to_one = []
            line = i.split("\t")
            go_id = line[0]
            description = "Description: " + line[2].split('"')[1]

            genes = line[1].split(",")
            gene_name = []
            for i in genes:
                gene = i.split(":")[1]
                gene_name.append(gene)
                unique_genes.append(gene)

            report_to_one.append(go_id)
            report_to_one.append(gene_name)
            report_to_one.append(description)

            report.append(report_to_one)

        unique_genes_dict["%s UNIQUE GENES" % (word.upper())] = Counter(unique_genes)
        interest_gene_dict["%s GENES ANNOTATION" % (word.upper())] = report

    
    with open(genes_analysis, "w") as fw:
        # GENES COUNTER
        with open(all_genes_file) as f:
            unknown_genes = 0
            known_genes = 0
            for line in f:
                line = line.strip()
                if line.startswith("#") or line.startswith("predicted"):
                    continue
                elif line == "":
                    unknown_genes += 1
                else:
                    known_genes += 1
        fw.write("Unnown genes: " + str(unknown_genes) + \
                 "\nKnown genes: " + str(known_genes) + \
                "\nGenes sum: " + str(unknown_genes + known_genes) + "\n")
        f.close()

        # UNIQUE GENES COUNTER
        for key, value in unique_genes_dict.items():
            fw.write("\n%s: " % key)
            for gene, number in dict(value).items():
                fw.write("\n%s : %s" % (gene, number))

        # WRITE INTERESTING GENES ANNOTATION INTO THE FILE
        for key, value in interest_gene_dict.items():
            fw.write("\n\n%s\n" % key)
            for gene_ann in value:
                go_id = gene_ann[0]
                genes = ", ".join(gene_ann[1])
                discription = gene_ann[2]
                fw.write("\n%s\t%s\t%s" % (go_id, genes, discription))
    fw.close()
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Eggnog annotation parser')
    parser.add_argument('-g','--gobo', help='whole path to go_obo', required=True)
    parser.add_argument('-e','--eggnog', help='whole path to eggnog-annotation file', required=True)
    parser.add_argument('-o','--output', help='output directory', required=True)
    args = vars(parser.parse_args())
    
    obo = args["gobo"]
    egg_anno = args["eggnog"]
    output = args["output"]
    prefix = egg_anno.split("/")[-1].split(".")[0]
    
    if output.endswith("/"):
        pass
    else:
        output = output + "/"
    
    main()