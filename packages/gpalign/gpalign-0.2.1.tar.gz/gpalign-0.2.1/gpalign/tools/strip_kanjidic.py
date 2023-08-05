#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  strip_kanjidic.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-05-23.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

import sys
import optparse

from cjktools.common import sopen
from cjktools import scripts

def transform_input(input_file, output_file):
    """
    Transforms each kanjidic entry into just the kanji to readings mapping.
    """
    istream = sopen(input_file, 'r')
    ostream = sopen(output_file, 'w')

    for line in istream:
        if line.startswith('#'):
            continue

        line = line.split()
        kanji = line[0]
        potential_readings = []
        for item in line[1:]:
            # lets not include radical names
            if item == 'T2':
                break
            else:
                if item.startswith('-'):
                    # ignore that item is a prefix
                    item = item[1:]
                elif item.endswith('-'):
                    # ignore that item is a suffix
                    item = item[:-1]
                if '.' in item:
                    # this marks that the second half is okurigana,
                    # skip the second half
                    item = item.split('.')[0]

                if scripts.script_type(item) == 'kanji':
                    # have non-kana item, must be ascii
                    continue
                else:
                    # have kana item, convert to katakana
                    potential_readings.append(scripts.to_katakana(item))

        print >> ostream, kanji, ' '.join(potential_readings)

    return

#----------------------------------------------------------------------------#

def create_option_parser():
    """ Creates an option parser instance to handle command-line options.
    """
    usage = \
"""%prog kanjidic_file output_file

Processes the kanjidic_file, stripping it of any excess information and
outputting the bare kanji -> readings mapping."""

    parser = optparse.OptionParser(usage)

    return parser

#----------------------------------------------------------------------------#

def main(argv):
    parser = create_option_parser()
    (options, args) = parser.parse_args(argv)

    try:
        [input_file, output_file] = args
    except:
        parser.print_help()
        sys.exit(1)

    transform_input(input_file, output_file)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

