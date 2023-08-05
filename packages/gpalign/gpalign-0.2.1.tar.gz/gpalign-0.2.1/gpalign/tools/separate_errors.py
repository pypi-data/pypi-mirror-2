#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  separate_errors.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-05-25.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

import sys
import optparse

from cjktools.common import sopen
from cjktools import scripts

def separate_alignments(alignment_file):
    """ Separates out the errors from the alignments, and tries to classify
        them.
    """
    input_file = sopen(alignment_file, 'r')
    good_file = sopen(alignment_file + '.good', 'w')
    okurigana_file = sopen(alignment_file + '.okurigana', 'w')
    gapping_file = sopen(alignment_file + '.gapping', 'w')
    bad_file = sopen(alignment_file + '.bad', 'w')

    n_good = 0
    n_bad = 0
    n_okurigana = 0
    n_gapping = 0
    for line in input_file:
        line_tuple = line.strip().split(':')
        if len(line_tuple) == 2:
            good_file.write(line)
            n_good += 1
        elif len(line_tuple) == 3:
            original, erronous, good = line_tuple
            if __detect_okurigana(good):
                n_okurigana += 1
                okurigana_file.write(line)
            elif __detect_gapping(good):
                n_gapping += 1
                gapping_file.write(line)
            else:
                bad_file.write(line)
            n_bad += 1
    
    total = n_good + n_bad
    n_unknown = n_bad - n_okurigana - n_gapping
    print '%d total alignments' % total
    print '--> %.2f%% correct (%d)' % ((100*n_good / float(total)),n_good)
    print '--> %.2f%% in error (%d)' % ((100*n_bad / float(total)),n_bad)
    print '----> %.2f%% okurigana (%d)' % ((100*n_okurigana / float(total)),\
            n_okurigana)
    print '----> %.2f%% gapping (%d)' % ((100*n_gapping / float(total)),\
            n_gapping)
    print '----> %.2f%% unknown (%d)' % ((100*(n_unknown)/float(total)),\
            n_unknown)

    return

#----------------------------------------------------------------------------#

def __detect_okurigana(segmentation):
    """ Detects whether the correct solution contained an okurigana segment.
        These are characterized by mixed script.
    """
    g_segments, p_segments = segmentation.split()
    g_segments = g_segments.strip('|').split('|')
    for segment in g_segments:
        script_type = scripts.script_type(segment[0])
        if script_type != 'kanji':
            continue

        for char in segment[1:]:
            if scripts.script_type(char) != 'kanji':
                return True
    else:
        return False

#----------------------------------------------------------------------------#

def __detect_gapping(segmentation):
    """ Determines whether this was a case of grapheme gapping. Tell-tale
        signs: a '<' in the phoneme segment.
    """
    g_segments, p_segments = segmentation.split()
    p_segments = p_segments.strip('|').split('|')
    for segment in p_segments:
        if '<' in segment:
            return True
    else:
        return False

#----------------------------------------------------------------------------#

def create_option_parser():
    usage = \
"""%prog [options] alignments

Separates out the different error types from the alignment file."""

    parser = optparse.OptionParser(usage)

    return parser

#----------------------------------------------------------------------------#

def main(argv):
    parser = create_option_parser()
    (options, args) = parser.parse_args(argv)

    try:
        [alignment_file] = args
    except:
        parser.print_help()
        sys.exit(1)

    separate_alignments(alignment_file)

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

