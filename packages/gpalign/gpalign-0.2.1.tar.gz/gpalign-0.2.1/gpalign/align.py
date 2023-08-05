#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  align.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-05-14.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 


"This module performs pure segmentation and alignment only."

import os
import sys
import optparse
import warnings

from consoleLog import default as _log

from gpalign import potentials
from gpalign import dictionary
from gpalign.alignment import AlignmentModel
from gpalign.reading_model import ReadingModel
from gpalign import evaluate
from gpalign import settings

def perform_segmentation(input_file, output_file, options):
    """ The main method for this module. Performs the entire segmentation run,
        taking an edict dictionary as input and producing a segmented output
        for each kanji input row.
    """
    steps = 4 if options.evaluate else 3
    _log.start('Aligning %s' % os.path.basename(input_file), nSteps=steps)
    
    _log.start('Setup phase', nSteps=4)
    
    _log.start('Reading entries')
    format = options.format
    if format == 'simple':
        entries, num_rejected = dictionary.evaluation_entries(input_file)
    elif format == 'edict':
        entries, num_rejected = dictionary.edict_entries(input_file)
    else:
        raise Exception('unknown format: %s' % format)
    
    _log.finish('Found %d entries (rejected %d)' % (len(entries),
            num_rejected))

    _log.start('Separating long and short entries')
    short_entries, long_entries = dictionary.separate_entries(entries,
            options.longest_run)
    _log.finish('%d short, %d long' % (len(short_entries), len(long_entries)))

    alignment_model = AlignmentModel(output_file, options)

    if options.use_kanjidic:
        reading_model = ReadingModel()
    else:
        reading_model = None
    _log.finish()
    _log.space()

    _log.start('Pass 1: short entries')
    _resolve_entries(alignment_model, reading_model, short_entries, options)
    _log.finish('Finished first pass')
    _log.space()

    _log.start('Pass 2: long entries')
    _resolve_entries(alignment_model, reading_model, long_entries, options)
    _log.finish('Finished second pass')

    alignment_model.finish()

    if options.evaluate:
        _log.space()
        evaluate.evaluate_alignment(output_file, output_file + '.eval')
        
    _log.finish()

#----------------------------------------------------------------------------#

def _resolve_entries(model, reading_model, entries, options):
    _log.start('Generating possible alignments')
    unique, ambiguous = potentials.generate_alignments(entries, options)
    _log.log('%d unique, %d ambiguous' % (len(unique), len(ambiguous)))
    _log.finish('%d overconstrained' % \
            (len(entries) - (len(unique) + len(ambiguous))))

    if options.use_kanjidic:
        _log.start('Disambiguating using kanjidic')
        more_unique, ambiguous = reading_model.prune_alignments(ambiguous)
        _log.finish('%d unique, %d ambiguous' % (len(more_unique),
                len(ambiguous)))
        unique.extend(more_unique)

    _log.start('Disambiguating readings using statistical model', nSteps=2)
    _log.log('Processing %d unique entries' % len(unique))
    model.add_resolved(unique)
    if ambiguous:
        _log.log('Disambiguating %d entries ' % len(ambiguous), newLine=False)
        model.disambiguate(ambiguous)
    _log.finish()

#----------------------------------------------------------------------------#
# COMMAND-LINE INTERFACE
#

def create_option_parser():
    """ Creates an option parser instance to handle command-line options.
    """
    usage = \
"""%prog [options] input_file output_file
       %prog [options] --evaluate

An efficient implementation of the Baldwin-Tanaka automated grapheme-phoneme
alignment algorithm based on TF-IDF. If passed --evaluate, it uses a bundled 
evaluation data set as input, and prints an accuracy analysis for the 
score."""

    parser = optparse.OptionParser(usage)

    parser.add_option('--max-per-kanji', action='store', dest='max_per_kanji',
            type='int', default=5,
            help='The maximum number of kana aligned to one kanji [5]')

    parser.add_option('--no-kanjidic', action='store_false',
            dest='use_kanjidic', default=True,
            help='Disables the kanjidic reading model')

    parser.add_option('--idf-only', action='store_false', dest='tf_heuristic',
            default=True, help='Only uses the idf heuristic [False]')

    parser.add_option('--tf-only', action='store_false', dest='idf_heuristic',
            default=True, help='Only uses the tf heuristic [False]')

    parser.add_option('--random', action='store_true', dest='random',
            help='Choose a random entry to disambiguate each time [False]')

    parser.add_option('--longest-run', action='store', dest='longest_run',
            type='int', default=4,
            help='The longest kanji run to be handled in the first pass [4]')

    parser.add_option('--format', action='store', dest='format',
            default='simple', 
            help='The format of the input file [simple]/edict')
    
    parser.add_option('--evaluate', action='store_true', dest='evaluate',
            help='Perform a run against the evaluation data.')

    parser.add_option('-a', '--alpha', action='store', dest='alpha',
            default=2.5, type='float',
            help='The smoothing value to use in tf-idf [2.5]')

    parser.add_option('-s', '--solved', action='store', dest='solved',
            default=0.07, type='float',
            help='The weight of solved frequencies in the tf-idf equation [0.07]')

    parser.add_option('-m', '--max-potentials', action='store',
            dest='max_potentials', type='int', default=120,
            help='The maximum number of potential alignments for an entry [120]')

    parser.add_option('--non-iterative', action='store_false',
            dest='iterative', default=True,
            help='Disables iterative alignment, instead taking one pass [False]')
    parser.add_option('-u', '--unsolved', action='store', dest='unsolved',
            default=0.13, type='float',
            help='The weight of unsolved frequencies in the tf-idf equation [0.13]')

    parser.add_option('--dump-model', action='store', dest='model_output',
            help="At the end of alignment, dump the model " + \
            "generated to the given file.")

    parser.add_option('--use-model', action='store', dest='model_input',
            help="Instead of generating a model, use this one.")

    return parser

#----------------------------------------------------------------------------#

def main(argv):
    parser = create_option_parser()
    (options, args) = parser.parse_args(argv)

    if options.random:
        options.tf_heuristic = False
        options.idf_heuristic = False
    
    if (options.evaluate and args) \
            or (not options.evaluate and len(args) != 2) \
            or options.format not in ('simple', 'edict'):
        parser.print_help()
        sys.exit(1)
    
    if options.evaluate:
        input_file = os.path.join(settings.DATA_DIR, 'eval-alignment.data')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            output_file = os.tempnam()    
    else:
        input_file, output_file = args
    
    perform_segmentation(input_file, output_file, options)
    
    if options.evaluate:
        os.remove(output_file)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        # we cancel runs often, so do it nicely
        print >> sys.stderr, '\nAborting run!'
        sys.exit(1)

#----------------------------------------------------------------------------#
