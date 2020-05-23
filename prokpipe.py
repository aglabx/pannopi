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

    workdir_list = []
    for i in os.listdir("data/"):
        if i.startswith("."):
            continue
        else:
            if os.path.isdir("data/" + i) == True:
                workdir_list.append(os.path.abspath("data/" + i))

    for workdir in workdir_list:
        #Reads prepare
        command = "tools/reads_prepare/reads_prepare.py"
        os.system(command)
        #Config-maker
        command = "config-maker.py -w %s -a %s -n %s" % (workdir, assembler, annotator)
        os.system(command)
        #Snakemake
        command = "snakemake --cores %s" % (threads)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('-a','--assembler', help='assebler tool: spades, unicycler or skesa', required=True)
    parser.add_argument('-n','--annotator', help='annotation tool: pgap or prokka', required=True)
    parser.add_argument('-t','--threads', help='number of threads', required=True)
    args = vars(parser.parse_args())

    assembler = args["assembler"]
    annotator = args["annotator"]
    threads = args["threads"]

    main()