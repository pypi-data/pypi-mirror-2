#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  detect_okurigana.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-05-14.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

"""
This module is an executable script performing grapheme-phoneme alignment
based on papers by Baldwin and Tanaka.
"""

import os, sys
import optparse

from okurigana_model import OkuriganaModel
import evaluate
import settings

def detect_okurigana(output_file, options):
    """ Performs just okurigana detection and alignment alteration.
    """
    okurigana_model = OkuriganaModel(options)

    input_file = options.input_file or os.path.join(settings.DATA_DIR,
            'eval-okurigana.data')
    okurigana_model.okurigana_adjustments(input_file, output_file)

    if not options.input_file:
        evaluate.evaluate_okurigana(output_file, output_file + '.eval')

def create_option_parser():
    """ Creates an option parser instance to handle command-line options.
    """
    usage = \
"""%prog [options] output_file

An efficient implementation of the Baldwin-Tanaka automated grapheme-phoneme
alignment algorithm based on TF-IDF."""

    parser = optparse.OptionParser(usage)

    parser.add_option('-t', '--threshold', action='store',
            dest='okuri_threshold', type='int', default=1,
            help='The threshold used for cooccurrence-based okurigana')

    parser.add_option('--simple', action='store_true',
            dest='simple_okurigana', default=False,
            help='Use a simple okurigana method, ignoring the main model')

    parser.add_option('--no-kanjidic', action='store_false',
            dest='use_kanjidic', default=True,
            help='Disables the kanjidic reading model')

    parser.add_option('--no-cooccurrence', action='store_false',
            dest='use_cooccurrence', default=True,
            help='Disables cooccurrence entries from edict')

    parser.add_option('--no-verbs', action='store_false',
            dest='use_verbs', default=True,
            help='Disables verb entries from edict')

    parser.add_option('-i', '--input', action='store', dest='input_file',
            help="Specify a custom input file to use.")

    return parser

def main(argv):
    """ The main method for this module.
    """
    parser = create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    output_file = args[0]

    detect_okurigana(output_file, options)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        # we cancel runs often, so do it nicely
        print >> sys.stderr, '\nAborting run!'
        sys.exit(1)
