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

    for i in os.listdir(workdir):
        if "R1" in i or "_1.fastq" in i:
            raw_fastq_1 = workdir + "/" + i
        elif "R2" in i or "_2.fastq" in i:
            raw_fastq_2 = workdir + "/" + i

    print("Forvard reads is:", raw_fastq_1)
    print("Reverse reads is:", raw_fastq_2)

    EXECUTE_INDEX_BUILDING = False

    if raw_fastq_1.endswith(".gz"):
        command = "gzip -d %s" % (raw_fastq_1)
        print(command)
        os.system(command)
        command = "gzip -d %s" % (raw_fastq_2)
        print(command)
        os.system(command)

        raw_fastq_1 = raw_fastq_1.replace(".gz", "")
        raw_fastq_2 = raw_fastq_2.replace(".gz", "")

    if raw_fastq_1.endswith(".tar.gz"):
        command = "tar xfvz %s" % (raw_fastq_1)
        print(command)
        os.system(command)
        command = "tar xfvz %s" % (raw_fastq_2)
        print(command)
        os.system(command)

        raw_fastq_1 = raw_fastq_1.replace(".tar.gz", "")
        raw_fastq_2 = raw_fastq_2.replace(".tar.gz", "")

    if raw_fastq_1.endswith(".fq"):
        new_raw_file_1 = raw_fastq_1.replace(".fq", ".fastq")
        command = "mv %s %s" % (raw_fastq_1, new_raw_file_1)
        print(command)
        os.system(command)
        new_raw_file_2 = raw_fastq_2.replace(".fq", ".fastq")
        command = "mv %s %s" % (raw_fastq_2, new_raw_file_2)
        print(command)
        os.system(command)
        raw_fastq_1 = new_raw_file_1
        raw_fastq_2 = new_raw_file_2

    if "R1" in raw_fastq_1:
        new_raw_file_1 = raw_fastq_1.split("R1")[0] + "_1.fastq"
        command = "mv %s %s" % (raw_fastq_1, new_raw_file_1)
        print(command)
        os.system(command)
        new_raw_file_2 = raw_fastq_2.split("R2")[0] + "_2.fastq"
        command = "mv %s %s" % (raw_fastq_2, new_raw_file_2)
        print(command)
        os.system(command)
        raw_fastq_1 = new_raw_file_1
        raw_fastq_2 = new_raw_file_2

    assert raw_fastq_1.endswith("_1.fastq")
    assert raw_fastq_2.endswith("_2.fastq")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('-w','--workdir', help='absolute path to working dir with raw reads', required=True)
    args = vars(parser.parse_args())

    workdir = args["workdir"]

    main()
