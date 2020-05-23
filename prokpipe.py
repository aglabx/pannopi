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

    workdir_list = os.listdir("data/")



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('-a','--assembler', help='assebler tool: spades, unicycler or skesa', required=True)
    parser.add_argument('-n','--annotator', help='annotation tool: pgap or prokka', required=True)
    args = vars(parser.parse_args())

    assembler = args["assembler"]
    annotator = args["annotator"]

    settings = {
        "work_dir": work_dir,
        "assembler": assembler,
        "annotator" : annotator
    }

    main(settings)
