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
        if "R1" in i:
            forward_reads = workdir + "/" + i
        elif "R2" in i:
            reverse_reads = workdir + "/" + i

    assert os.path.exists(forward_reads)
    assert os.path.getsize(forward_reads) > 0

    raw_reads1 = os.path.split(forward_reads)[1]
    raw_reads2 = os.path.split(reverse_reads)[1]

    if raw_reads1.endswith(".gz"):
        command = "gunzip {forward_reads}".format(forward_reads = forward_reads)
        print(command)
        os.system(command)
    if raw_reads2.endswith(".gz"):
        command = "gunzip {reverse_reads}".format(reverse_reads = reverse_reads)
        print(command)
        os.system(command)
    if "R1" in raw_reads1:
        forward_reads1 = forward_reads.split("R1")[0] + "1.fastq"
        command = "mv %s %s" % (forward_reads, forward_reads1)
        print(command)
        os.system(command)
    if "R2" in raw_reads2:
        reverse_reads2 = reverse_reads.split("R2")[0] + "2.fastq"
        command = "mv %s %s" % (reverse_reads, reverse_reads2)
        print(command)
        os.system(command)

    forward_reads = forward_reads1
    reverse_reads = reverse_reads2

    assert forward_reads.endswith("_1.fastq")
    assert reverse_reads.endswith("_2.fastq")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('-w','--workdir', help='working dir with raw reads', required=True)
    args = vars(parser.parse_args())

    work_dir = args["workdir"]

    main()
