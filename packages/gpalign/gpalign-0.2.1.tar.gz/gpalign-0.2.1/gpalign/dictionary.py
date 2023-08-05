# -*- coding: utf-8 -*-
# 
#  dictionary.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-05-16.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

"""
This module is responsible for parsing input data sets for grapheme/phoneme
string pairs to align. Its main methods are edict_entries() and
evaluation_entries().
"""

from cjktools import scripts
from cjktools.common import sopen

from entry import Entry
import settings

def edict_entries(input_file):
    """
    Determines all the kanji entries available in the input file. The
    input file is assumed to be in edict format.
    """
    istream = sopen(input_file)
    log_stream = settings.LogStream.get()
    
    entries = []
    num_rejected = 0
    for line in istream:
        parts = line.split()
        g_string = parts[0]
        p_string = parts[1][1:-1]
        
        if _valid_entry(g_string, p_string):
            entries.append(Entry(g_string, p_string))
        else:
            num_rejected += 1
            log_stream.log_rejected(line.rstrip())

    return entries, num_rejected

def evaluation_entries(input_file):
    """ Get entries from a file formatted like an evaluation type instead of
        in edict format.
    """
    entries = []
    istream = sopen(input_file, 'r')

    log_stream = settings.LogStream.get()

    num_rejected = 0
    for line in istream:
        g_string, p_string = line.split(':')[0].split()
        
        if _valid_entry(g_string, p_string):
            entries.append(Entry(g_string, p_string))
        else:
            num_rejected += 1
            log_stream.log_rejected(line.rstrip())

    return entries, num_rejected

def separate_entries(entries, max_run_length=3):
    """ Split out the longest entries for later processing.
    """
    short_entries = []
    long_entries = []

    for entry in entries:
        if _longest_kanji_run(entry.g_string) > max_run_length:
            long_entries.append(entry)
        else:
            short_entries.append(entry)
    
    return short_entries, long_entries

#----------------------------------------------------------------------------#

def _valid_entry(g_string, p_string):
    """ Returns True if the word is only kanji and kana, False otherwise.
    """
    # throw out any grapheme string which contains ascii
    if scripts.Script.Ascii in map(scripts.script_type, g_string): 
        return False

    # throw out any reading which non-kana readings
    isKana = lambda x: x in (scripts.Script.Hiragana, scripts.Script.Katakana)

    has_non_kana = (filter(isKana, map(scripts.script_type, p_string)) != [])

    return has_non_kana

def _longest_kanji_run(g_string):
    """ Works out the longest number of kanji in a row in the grapheme string.
    """
    run = 0
    longest = 0
    kanji_script = scripts.Script.Kanji
    for char in g_string:
        if scripts.script_type(char) == kanji_script:
            run += 1
        else:
            if run > longest:
                longest = run
            run = 0
    else:
        if run > longest:
            longest = run
    
    return longest

