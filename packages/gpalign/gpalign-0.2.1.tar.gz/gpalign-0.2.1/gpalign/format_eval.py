#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  format_eval.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-09-07.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

import sys
import optparse
from cjktools.common import sopen

from entry import Entry

def format_eval_file(input_file, output_file):
    entries = _parse_entries(input_file)
    ostream = sopen(output_file, 'w')

    for entry in entries:
        line_a = entry.g_string.ljust(10, u'　')
        line_b = entry.p_string.ljust(10, u'　')

        extra_a, extra_b = _match_alignments(entry.alignments[0])
        line_a += extra_a.ljust(10, u'　')
        line_b += extra_b.ljust(10, u'　')

        extra_a, extra_b = _match_alignments(entry.alignments[1])
        line_a += extra_a.ljust(10, u'　')
        line_b += extra_b.ljust(10, u'　')

        print >> ostream, line_a
        print >> ostream, line_b
        print >> ostream

    ostream.close()

def _match_alignments(alignment):
    g_segments, p_segments = map(list, alignment)
    for i in range(len(g_segments)):
        g_segments[i] = g_segments[i].ljust(len(p_segments[i]), u'　')

    line_a = u'｜'.join(g_segments)
    line_b = u'｜'.join(p_segments)

    return line_a, line_b

def _parse_entries(input_file):
    entries = []
    for line in sopen(input_file, 'r'):
        base, attempt, actual = line.strip().split(':')

        g_string, p_string = base.split()
        entry = Entry(g_string, p_string)
        fixify = lambda x: map(lambda y: y.strip('|').split('|'), 
                x.split())
        attempt = fixify(attempt)
        actual = fixify(actual)

        entry.alignments=[attempt, actual]
        
        entries.append(entry)

    return entries

def create_option_parser():
    usage = "%prog [options] input_file output_file"

    parser = optparse.OptionParser(usage)

    return parser

def main(argv):
    parser = create_option_parser()
    (options, args) = parser.parse_args(argv)

    try:
        [input_file, output_file] = args
    except:
        parser.print_help()
        sys.exit(1)

    format_eval_file(input_file, output_file)

if __name__ == '__main__':
    main(sys.argv[1:])

# vim: ts=4 sw=4 sts=4 et tw=78: