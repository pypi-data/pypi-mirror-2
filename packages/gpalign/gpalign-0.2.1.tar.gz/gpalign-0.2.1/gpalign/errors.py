#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  errors.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-05-25.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

import okurigana_model

from cjktools.common import sopen

def separate_errors(base_file):
    """
    Separates out the errors from the alignments, and tries to classify them.
    """
    input_file = sopen(base_file, 'r')

    good = set()
    bad = set()
    bad_okuri = set()
    bad_gapping = set()
    bad_align = set()
    bad_constrain = set()

    for line in input_file:
        original, test_case, correct_case = _parse_line(line)

        if test_case == correct_case:
            good.add(line)
            continue

        if test_case == [('???',)]:
            bad_constrain.add(line)
            bad.add(line)
            continue

        # the rest of the cases are bad
        if _detect_gapping(correct_case):
            bad_gapping.add(line)
            bad.add(line)
            continue

        if _bad_alignment(test_case, correct_case):
            bad_align.add(line)

        elif _bad_okurigana(correct_case, test_case):
            bad_okuri.add(line)

        bad.add(line)
    
    total = len(good.union(bad))
    bad_other = bad.difference(bad_gapping.union(bad_align).union(
            bad_okuri).union(bad_constrain))

    _lines_to_file(good, '.good', base_file)
    _lines_to_file(bad, '.bad', base_file)
    _lines_to_file(bad_okuri, '.bad.okuri', base_file)
    _lines_to_file(bad_gapping, '.bad.gapping', base_file)
    _lines_to_file(bad_align, '.bad.align', base_file)
    _lines_to_file(bad_other, '.bad.other', base_file)
    _lines_to_file(bad_constrain, '.bad.constrain', base_file)

    (n_good, n_bad, n_bad_okuri, n_bad_gapping, n_bad_align, n_unknown,
            n_constrain) = \
            map(
                len,
                (good, bad, bad_okuri, bad_gapping, bad_align, bad_other,
                bad_constrain)
            )

    print '%d total alignments' % total
    print '--> %.2f%% correct (%d)' % ((100*n_good / float(total)),n_good)
    print '--> %.2f%% in error (%d)' % ((100*n_bad / float(total)),n_bad)
    print '----> %.2f%% okurigana (%d)' % ((100*n_bad_okuri / float(total)),\
            n_bad_okuri)
    print '----> %.2f%% gapping (%d)' % ((100*n_bad_gapping / float(total)),\
            n_bad_gapping)
    print '----> %.2f%% align (%d)' % ((100*n_bad_align / float(total)),\
            n_bad_align)
    print '----> %.2f%% overconstrained (%d)' % ((100*n_constrain / \
            float(total)), n_constrain)
    print '----> %.2f%% unknown (%d)' % ((100*(n_unknown)/float(total)),\
            n_unknown)

#----------------------------------------------------------------------------#

def _parse_line(line):
    line_tuple = line.strip().split(':', 2)

    segment = lambda x: tuple(x.strip('|').split('|'))
    line_tuple = map(lambda x: map(segment, x.split(' ',1)), line_tuple)

    return line_tuple

#----------------------------------------------------------------------------#

def _lines_to_file(line_set, extension, base_name):
    ostream = sopen(base_name + extension, 'w')
    ostream.writelines(line_set)
    ostream.close() 

#----------------------------------------------------------------------------#

def _bad_alignment(test_case, correct_case):
    """ Determines whether this case is a bad alignment case.
    """
    g_segments, p_segments = test_case
    cg_segments, cp_segments = correct_case

    if okurigana_model.alignment_has_okurigana(cg_segments, cp_segments):
        test_case = okurigana_model.remove_okurigana(test_case[0],
                test_case[1])
        correct_case = okurigana_model.remove_okurigana(correct_case[0],
                correct_case[1])

    return test_case != correct_case

#----------------------------------------------------------------------------#

def _bad_okurigana(test_case, correct_case):
    g_segments, p_segments = test_case
    cg_segments, cp_segments = correct_case

    if okurigana_model.alignment_has_okurigana(cg_segments, cp_segments):
        if okurigana_model.alignment_has_okurigana(g_segments, p_segments):
            return True
        else:
            # we forgot to add okurigana
            return False
    else:
        # have we mistakenly added okurigana?
        return okurigana_model.alignment_has_okurigana(g_segments, p_segments)

#----------------------------------------------------------------------------#

def _detect_gapping(correct_case):
    """ Determines whether this was a case of grapheme gapping. Tell-tale
        signs: a '<' in the phoneme segment.
    """
    g_segments, p_segments = correct_case
    for segment in p_segments:
        if '<' in segment:
            return True
    else:
        return False

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:
