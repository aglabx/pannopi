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
    parser.add_argument('-a','--assembler', help='assebler tool: spades, unicycler or skesa [default = spades]', default="spades")
    parser.add_argument('-n','--annotator', help='annotation tool: pgap or prokka [default = prokka]', default="prokka")
    parser.add_argument('-c','--cpus', help='number of threads [default = 8]', default="8")
    parser.add_argument('-t','--test', help='run pipeline on test data', action='store_true')
    parser.add_argument('-d','--debug', help='debug mode', action='store_true')
    args = vars(parser.parse_args())

    assembler = args["assembler"]
    annotator = args["annotator"]
    cpus = args["cpus"]
    test = args["test"]
    debug = args["debug"]

    main()
