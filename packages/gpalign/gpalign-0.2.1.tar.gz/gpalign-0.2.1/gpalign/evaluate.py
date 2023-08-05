#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  evaluate.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-08-12.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

import os, sys
import optparse
import operator

from simplestats import sequences
from cjktools.common import sopen
from consoleLog import default as _log

import errors
import settings

#----------------------------------------------------------------------------#

def evaluate_alignment(prediction_file, results_file):
    """ Evaluates the alignments provided in the prediction file, writing the
        results to the results file.
    """
    validation_file = os.path.join(settings.DATA_DIR, 'eval-alignment.data')

    results = {}

    validation_cases = _list_entries(validation_file)
    validation_dict = dict(validation_cases)

    prediction_cases = _list_entries(prediction_file)
    prediction_dict = dict(prediction_cases)

    matching = lambda x: x in validation_cases
    good, bad = sequences.separate(matching, prediction_cases)

    results['good'] = good

    add_correct = lambda x: x + (validation_dict[x[0]],)
    bad = map(add_correct, bad)

    results['bad'] = bad

    has_gapping = lambda x: reduce(
            operator.or_,
            map(lambda y: '<' in y, x[2])
        )
    gapping, align = sequences.separate(has_gapping, bad)

    results['gapping'] = gapping
    results['align'] = align

    is_missing = lambda x: not prediction_dict.has_key(x[0])
    missing = filter(is_missing, validation_cases)
    results['missing'] = missing

    _write_results(results, results_file)
    _log_results(results)

#----------------------------------------------------------------------------#

def evaluate_okurigana(prediction_file, results_file):
    """ Evaluates the alignments provided in the prediction file, writing the
        results to the results file.
    """
    validation_file = os.path.join(settings.DATA_DIR, 'eval-okurigana.data')

    results = {}

    validation_cases = _list_entries(validation_file)
    validation_dict = dict(validation_cases)

    prediction_cases = _list_entries(prediction_file)
    prediction_dict = dict(prediction_cases)

    matching = lambda x: x in validation_cases
    good, bad = sequences.separate(matching, prediction_cases)

    results['good'] = good

    add_correct = lambda x: x + (validation_dict[x[0]],)
    bad = map(add_correct, bad)

    results['okuri'] = bad

    is_missing = lambda x: not prediction_dict.has_key(x[0])
    missing = filter(is_missing, validation_cases)
    results['missing'] = missing

    results['bad'] = bad + missing

    _write_results(results, results_file)
    _log_results(results)

#----------------------------------------------------------------------------#

def _write_results(results_dict, results_file):
    keys = results_dict.keys()
    keys.sort()

    summary_stream = open(results_file, 'w')

    for key in keys:
        key_entries = results_dict[key]
        number = len(key_entries)
        percent = 100.0*number/5000.0
        print >> summary_stream, '%s    %4d    %6.2f%%' % (key, number,
                percent)

        ostream = sopen(results_file + '.' + key, 'w')
        for line in key_entries:
            print >> ostream, ':'.join(line)
        ostream.close()

#----------------------------------------------------------------------------#

def _log_results(results_dict):
    _log.start('Evaluating alignments', nSteps=2)

    good = len(results_dict['good'])
    _log.log('good: %d (%.02f%%)' % (good, 100.0 * good / 5000.0))
    bad = len(results_dict['bad'])
    _log.start('bad: %d (%.02f%%)' % (bad, 100.0 * bad / 5000.0))
    align = len(results_dict['align'])
    _log.log('bad alignment: %d (%.02f%%)' % (align, 100.0 * align / 5000.0))
    gapping = len(results_dict['gapping'])
    _log.log('gapping: %d (%.02f%%)' % (gapping, 100.0 * gapping / 5000.0))
    missing = len(results_dict['missing'])
    _log.finish('missing: %d (%.02f%%)' % (missing, 100.0 * missing / 5000.0))
    
    _log.finish()

#----------------------------------------------------------------------------#


def _list_entries(filename):
    entries = []
    istream = sopen(filename, 'r')

    for line in istream:
        key, value = line.strip().split(':', 1)
        entries.append((key, value))

    istream.close()

    return entries

#----------------------------------------------------------------------------#

def evaluate(prediction_file, validation_file, validation_results):
    """ Evaluates the predictions against the validation data, writing the
        output to a series of files with basename validation_results.
    """
    test_entries = _get_entries(prediction_file)
    correct_entries = _get_entries(validation_file)

    _compare_entries(test_entries, correct_entries, validation_results)

    # split the errors into a detailed analysis
    errors.separate_errors(validation_results)

#----------------------------------------------------------------------------#

def _get_entries(filename):
    """ Creates a dictionary of all the entries in the given file.
    """
    lines = sopen(filename, 'r').readlines()

    entries = {}
    for line in lines:
        key, value = line.split(':')[:2]
        entries[key] = value.strip()

    return entries

#----------------------------------------------------------------------------#

def _compare_entries(test_entries, correct_entries, result_file):
    """ Compares the entries from the different files.
    """
    n_lines = 0
    n_correct = 0
    n_missing = 0
    ostream = sopen(result_file, 'w')
    for key, alignment in correct_entries.iteritems():
        test_alignment = test_entries.get(key, '???')

        if alignment == test_alignment:
            n_correct += 1

        if test_alignment == '???':
            n_missing += 1

        print >> ostream, '%s:%s:%s' % (key, test_alignment, alignment)

        n_lines += 1
    
    ostream.close()

    print 'Got %.2f%% correct!' % (n_correct*100.0/n_lines)
    if n_missing > 0:
        print '   but %d were missing...' % n_missing

#----------------------------------------------------------------------------#

def sort_file(filename):
    istream = sopen(filename, 'r')
    lines = istream.readlines()
    istream.close()

    lines.sort()

    ostream = sopen(filename, 'w')
    ostream.writelines(lines)
    ostream.close()

def create_option_parser():
    usage = "%prog [options] rawResults adjustedResults"

    parser = optparse.OptionParser(usage)

    
    parser.add_option('-e', action='store', dest='correct_file',
        default=os.path.join(settings.DATA_DIR, 'evaluation.data'),
        help='The file of correct evaluations')

    return parser

def main(argv):
    parser = create_option_parser()
    (options, args) = parser.parse_args(argv)

    try:
        [test_output_file, results_file] = args
    except:
        parser.print_help()
        sys.exit(1)

    evaluate(test_output_file, options.correct_file, results_file)

if __name__ == '__main__':
    main(sys.argv[1:])

# vim: ts=4 sw=4 sts=4 et tw=78: