#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: <data>
#@author: <name>
#@contact: <email>

import sys
import argparse
import os
import os.path
from collections import Counter


def main():
    ''' Function description.
    '''
    # ПЕРВАЯ СТАДИЯ, ЧИТАЕМ БЛАСТ, НАХОДИМ ДЛИНУ УЧАСТКОВ ПО БАКТЕРИЯМ И ТАКСОНАМ

    bact_taxid = {}
    contigs = {} # ЗАПИСАВАЕМ КОНТИГИ В СЛОВАРЬ, ДАЛЬШЕ ЕГО ИСПОЛЬЗУЕМ ДЛЯ ПОИСКА КОНТАМИНАЦИЙ

    vectors = []
    phages = []

    bact_length = Counter()
    taxid_length = Counter()
    total_length = 0

    bact_seq = {}
    with open(blastn_taxid_out) as fh:
        for line in fh:
            line = line.strip().split("\t")
            #Column names
            contig = line[0]
            contigs[contig] = []
            ident = float(line[2])
            start = line[3]
            end = line[4]
            length = int(line[5])
            bact_full_name = line[7]
            bacteria = " ".join(line[7].split(" ")[:2])
            taxid = line[8]

            if "vector" in bact_full_name or "Vector" in bact_full_name:
                vectors.append(line)
            if "phage" in bact_full_name or "Phage" in bact_full_name:
                phages.append(line)

            bact_length[bacteria] += length
            taxid_length[taxid] += length
            total_length += length

            bact_seq[bacteria] = contig + ":" + start + ".." + end
            
    # ШАГ 2. НАХОДИМ НАЗВАНИЕ НАШЕЙ БАКТЕРИИ И ЕЕ ТАКСОН 

    target_bact_seq = {}
    bact_perc = Counter()
    for bact, length in bact_length.most_common():
        bact_perc[bact] = length/total_length * 100

    target_bact_sciname = bact_perc.most_common(1)[0][0]

    print("\nBACTERIAL CONTENT IS:", bact_perc.most_common(5))
    print("\nMOST COMMON TAXON id IS:", taxid_length.most_common(5))

    bacteria_id = []
    for i in taxid_length.most_common()[:3]:
        bacteria_id.append(str(i[0]) + " = " + str(i[1]/total_length * 100) + "%")

    # ШАГ 3. ЗАПИСЫВАЕМ КОНТАМИНАЦИИ В СЛОВАРЬ

    for node, position in contigs.items():
        with open(blastn_taxid_out) as fh:
            for line in fh:
                line = line.strip().split("\t")

                #column names
                contig = line[0]
                ident = float(line[2])
                start = line[3]
                end = line[4]
                bacteria = " ".join(line[7].split(" ")[:2])

                if contig == node and bacteria != target_bact_sciname and ident > 80:
                    if start + ":" + end + ":" + bacteria in position:
                        continue
                    else:
                        position.append(start + ":" + end + ":" + bacteria)
                    break
            fh.close()
           
      #ФИЛЬТРУЕМ НАЙДЕННЫЕ КОНТАМИНАЦИИ, ВЛОЖЕННЫЕ УДЛИННЯЕМ
    delete_seq = {}

    for node, position in contigs.items():
        if position:
            position.sort(key=lambda x : (int(x.split(":")[0]), -1 * int(x.split(":")[1])))
            delete_seq[node] = []

            i = 1
            ps,pe = map(int, position[0].split(":")[:2])
            bac = position[i-1].split(":")[2]
            while i < len(position):
                bac = position[i-1].split(":")[2]
                s,e = map(int, position[i].split(":")[:2])
                if pe + 1 < s:
                    delete_seq[node].append((ps, pe, bac))
                    ps, pe = s, e
                    i += 1
                    continue

                pe = max(e, pe)
                i += 1
            delete_seq[node].append((ps, pe, bac))

    # ШАГ 4, УДАЛЯЕМ АДАПТЕРЫ И ПОСЛЕ ЭТОГО КОНТИГИ ДЛИНОЙ МЕНЬШЕ 200 БП

    # БЛАСТИМ ГЕНОМ НА АДАПТЕРЫ

    if not os.path.exists(adapters_report):
        os.system("touch %s" % adapters_report)
    
    command = """
    blastn -query %s \
                        -db %s \
                        -outfmt 6 \
                        -max_target_seqs 1000 \
                        -task blastn \
                        -reward 1 \
                        -penalty \
                        -5 \
                        -gapopen 3 \
                        -gapextend 3 \
                        -dust yes \
                        -soft_masking true \
                        -evalue 0.00001 \
                        -searchsp 1750000000000 \
                        -out %s
              """ % (scaffold, adapters_db, adapters_report)
    
    print(command)
    os.system(command)
    
    adapters_to_del = {}
    with open(adapters_report) as fh:
        for line in fh:
            line = line.strip().split()
            ids = line[1].split(":")[1]
            contig = line[0]
            start = line[6]
            stop = line[7]
            adapters_to_del[contig] = start + ":" + stop
    
    print("\n" + str(len(adapters_to_del)) + " ADAPTERS WERE FOUND! DELETING...")

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
    
    for contig, position in adapters_to_del.items():
        start = int(position.split(":")[0])-1
        stop = int(position.split(":")[1])
        for key, value in fasta.items():
            if key.startswith(">" + contig):
                line_to_del = value[start:stop]
                value = value.replace(line_to_del, "")
                fasta[key] = value
    
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
    
    with open(contera_report, 'w') as fw:
        fw.write("BACTERIAL CONTENT OF ASSEMBLY IS:\n")
        for i in bact_perc.most_common(5):
            bact = str(i[0])
            perc = str(i[1])
            fw.write(bact + " - " + perc +"%\n")

        fw.write("\nTHE MOST COMMON ID IS :\n" + ", ".join(bacteria_id) + "\n\n")

        fw.write("FOREIGN BACTERIA SITES:\n")
        for node, position in delete_seq.items():
            fw.write(node + "\t")
            for i in position:
                start_to_stop = ":".join(str(number) for number in i[:2])
                bacteria = i[2]
                fw.write(start_to_stop + "\t" + bacteria + "\n")

        fw.write("\n" + str(len(adapters_to_del)) + " ADAPTERS WERE REMOVED IN:\n")
        for node, position in adapters_to_del.items():
            fw.write(node + "\t" + position + "\n")

        fw.close()
        
        print("\nCOMPLETED SUCCESSFULLY!\n\nRESULTS FILE LAYS IN " + contera_report)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Bacterial genome contamination erasing tool')
    parser.add_argument('-s','--scaffold', help='whole path to scaffold_file', required=True)
    parser.add_argument('-b','--blastn', help='whole path to outfmt6 file', required=True)
    parser.add_argument('-a','--adapters', help='whole path to adapters database in fasta format', required=True)
    parser.add_argument('-o','--output', help='output_path', required=True)
    args = vars(parser.parse_args())
    
    scaffold = os.path.abspath(args["scaffold"])
    blastn_taxid_out = os.path.abspath(args["blastn"])
    adapters_db = os.path.abspath(args["adapters"])
    output = os.path.abspath(args["output"]) + "/"
    scaforarg = scaffold.split("/")[-1].split(".")[0]
    prefix = blastn_taxid_out.split("/")[-1].split(".")[0]
    
    scaffolds_filtered = output + scaforarg + "_filtered.fasta"
    contera_report = output + prefix + ".contera_report.txt"
    adapters_report = output + prefix + ".adapters_report.outfmt6"
    
    main()
