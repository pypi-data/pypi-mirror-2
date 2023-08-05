# -*- coding: utf-8 -*-
# 
#  potentials.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-05-15.
#  Copyright 2010 Lars Yencken. All rights reserved.
# 

"""
This module is responsible for generating all possible segmentations for
each grapheme string/phoneme string pair. The main method exported is the
generate_alignments() method.
"""

import string
import sys

from cjktools import scripts, kana_table
from simplestats import comb

import settings

#----------------------------------------------------------------------------#
# PUBLIC METHODS
#

def generate_alignments(entries, options):
    """ Generates all possible alignments for each entry/reading pair in the
        input list.

        @param entries: A list of (grapheme string, phoneme string) pairs.
        @type entries: [(str, str)]
        @return: A pair (unique alignments, ambiguous alignments) where the
        second member is a list of (graphemeString, [potentialAlignments]).
    """
    # we record anything which we've overconstrained and can't solve
    log_stream = settings.LogStream.get()

    unique_entries = []
    ambiguous_entries = []

    for entry in entries:
        _add_alignments_to_entry(entry, options)

        if entry.aligned:
            unique_entries.append(entry)
            continue

        if entry.potentials:
            ambiguous_entries.append(entry)
        else:
            # we've overconstrained this entry -- no potential alignments
            log_stream.log_overconstrained(entry)
    
    return unique_entries, ambiguous_entries

#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# PRIVATE METHODS
#

def _add_alignments_to_entry(entry, options):
    """ Determine all possible kanji/reading segmentations and aligments,
        taking linguistic constraints into account.
    """
    # work out all the ways the grapheme string can vary
    partial_alignments = _grapheme_alignments(entry.g_string)

    if len(partial_alignments) > 0.75*options.max_potentials:
        # too many alignments
        return

    # for each grapheme variation, work out possible phonetic alignments
    final_alignments = _phoneme_alignments(entry.p_string, partial_alignments,
            options)

    if len(final_alignments) > options.max_potentials:
        # too many alignments
        return

    assert len(set(final_alignments)) == len(final_alignments), \
            "duplicate alignments detected"

    if len(final_alignments) == 1:
        entry.aligned = True
        entry.alignment = final_alignments[0]
    else:
        entry.potentials = final_alignments

#----------------------------------------------------------------------------#

def _grapheme_alignments(g_string):
    """ Determine all possible segmentations of the mixed script entry string
        only, leaving the hiragana reading string untouched for now.
    """
    kanji_script = scripts.Script.Kanji
    combination_sets = []
    for segment in scripts.script_boundaries(g_string):
        if len(segment) > 1 and scripts.script_type(segment) == kanji_script:
            combination_sets.append(comb.segment_combinations(segment))
        else:
            combination_sets.append([(segment,)])
    
    alignments = comb.combination_seqs(*combination_sets)

    return alignments

#----------------------------------------------------------------------------#

def _phoneme_alignments(p_string, partial_alignments, options):
    """ For each segmented kanji string, this method segments the reading to
        match.
    """
    alignments = []
    for grapheme_segments in partial_alignments:
        alignments.extend(_match_grapheme_segments(p_string,
                grapheme_segments))
    
    alignments = _prune_alignments(alignments, options)

    return alignments

#----------------------------------------------------------------------------#

def _match_grapheme_segments(p_string, g_segments):
    """ Creates one or more segmentations which match the kanji segments with
        the reading string.
    """
    kanji_script = scripts.Script.Kanji

    # where there's only one segment, no worries
    num_segments = len(g_segments)
    if num_segments == 1:
        p_segments = (p_string,)
        return [(g_segments, p_segments)]

    p_segments_list = [((), p_string)]
    for i in range(num_segments):
        g_segment = g_segments[i]
        # FIXME is this needed? finalSegment = (num_segments == i+1)

        if scripts.script_type(g_segment) == kanji_script:
            p_segments_list = _align_kanji_segment(g_segment, p_segments_list,
                    i, num_segments)
        else:
            p_segments_list = _align_kana_segment(g_segment, p_segments_list)
    
    # filter out those with remaining unaligned phonemes
    alignments = [(g_segments, x) for (x,y) in p_segments_list if y == '']

    return alignments

#----------------------------------------------------------------------------#

def _align_kanji_segment(g_segment, p_segments_list, i, num_segments):
    """ Align an individual kanji segment with each of several possible
        phoneme alignments.
    """
    next_level_segments = []

    # for each potential, generate many possible alignments
    for existing_segments, remaining_reading in p_segments_list:
        # at least one phoneme for every grapheme
        max_seg_length = len(remaining_reading) + i - num_segments + 1
        min_seg_length = len(g_segment)

        # add a possible alignment for each slice of kana pie
        for j in range(min_seg_length, max_seg_length+1):
            new_segments = existing_segments + (remaining_reading[:j],)
            new_remaining_reading = remaining_reading[j:]
            next_level_segments.append((new_segments, new_remaining_reading))
    
    return next_level_segments

#----------------------------------------------------------------------------#

def _align_kana_segment(g_segment, p_segments_list):
    """ Align with a kana segment, which has to match up with itself. Discard
        any potential alignments where this kana doesn't match up.
    """
    seg_len = len(g_segment)

    next_level_segments = []
    for p_segments, p_string in p_segments_list:
        if p_string[:seg_len] == g_segment:
            p_segments += (g_segment,)
            p_string = p_string[seg_len:]
            next_level_segments.append((p_segments, p_string))

    return next_level_segments

#----------------------------------------------------------------------------#

def _prune_alignments(alignments, options):
    """ Applies additional constraints to the list of alignments, returning a
        subset of that list.
    """
    kanji_script = scripts.Script.Kanji
    kept_alignments = []
    for kanji_seg, reading_seg in alignments:
        assert len(kanji_seg) == len(reading_seg)
        for i in range(len(reading_seg)):
            r_seg = reading_seg[i]
            k_seg = kanji_seg[i]

            # don't allow reading segments to start with ゅ or ん
            if scripts.script_type(k_seg) == kanji_script and (
                        r_seg[0] == kana_table.n_kana \
                        or r_seg[0] in kana_table.small_kana
                    ):
                break

            # don't allow kanji segments with more than 4 kana per kanji
            r_seg_short = filter(lambda x: x not in kana_table.small_kana,
                    r_seg)
            max_length = options.max_per_kanji*len(k_seg)
            if scripts.script_type(k_seg) == kanji_script and \
                    len(r_seg_short) > max_length:
                break
        else:
            kept_alignments.append((kanji_seg, reading_seg))

    return kept_alignments

#----------------------------------------------------------------------------#

def segment_to_string(segment):
    return string.join(segment, '|')

#----------------------------------------------------------------------------#

def alignment_to_string(alignment):
    return segment_to_string(alignment[0]) +' - '+ \
            segment_to_string(alignment[1])

#----------------------------------------------------------------------------#

def print_segment(segment, stream=sys.stdout):
    print >> stream, string.join(segment, '|')
    return

#----------------------------------------------------------------------------#

def print_alignment(alignment, stream=sys.stdout):
    print >> stream, '|'.join(alignment[0]) + ' - ' + '|'.join(alignment[1])
    return

#----------------------------------------------------------------------------#

