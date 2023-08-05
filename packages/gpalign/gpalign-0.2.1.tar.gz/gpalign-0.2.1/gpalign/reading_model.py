# -*- coding: utf-8 -*-
# 
#  reading_model.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-08-18.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

from cjktools import scripts, enum, alternations
from cjktools.resources import kanjidic
from simplestats.sequences import flatten
from consoleLog import default as _log

#----------------------------------------------------------------------------#

class PathException(Exception): pass

#----------------------------------------------------------------------------#

ReadingLoc = enum.Enum('any', 'prefix', 'suffix')
ReadingType = enum.Enum('on', 'kun', 'unknown')
ReadingKnowledge = enum.Enum('known', 'trial')

#----------------------------------------------------------------------------#

class ReadingModel:
    """
    A model of the readings that each kanji takes, and some additional
    information on their reliability. 
    """

    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #

    def __init__(self):
        """
        Creates a new instance, populating it with kanjidic's model. The
        initial model gets cached, so we don't have to get any differences.
        """
        _log.log('Initialising reading model')
        self._readings = {}
        self._pool = {}
        self._okuri = {}
        
        model = self._parse_kanjidics()

        self._readings, self._pool, self._okuri = model

    #------------------------------------------------------------------------#

    def prune_alignments(self, ambiguous_entries):
        """ Prunes potential alignments away from entries where.
        """
        unique = []
        ambiguous = []
        kanji_script = scripts.Script.Kanji
        for entry in ambiguous_entries:
            remaining_alignments = []

            for g_segments, p_segments in entry.potentials:
                for i in xrange(len(g_segments)):
                    if not scripts.script_type(g_segments[i]) == kanji_script:
                        continue

                    if not self._validate_reading(g_segments[i],
                            p_segments[i]):
                        # hit a bad reading, skip this alignment
                        break
                else:
                    # all readings matched
                    remaining_alignments.append((g_segments, p_segments))

            if not remaining_alignments:
                # this method failed, fallback to previous method
                ambiguous.append(entry)
            elif len(remaining_alignments) == 1:
                # success, disambiguated
                entry.potentials = []
                [entry.alignment] = remaining_alignments
                entry.aligned = True
                unique.append(entry)
            else:
                # success, partially disambiguated
                entry.potentials = remaining_alignments
                ambiguous.append(entry)

        return unique, ambiguous

    #------------------------------------------------------------------------#

    def get_okurigana(self):
        return self._okuri

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #

    def _validate_reading(self, grapheme, phoneme):
        """ Checks whether a given grapheme/phoneme pair are matched up in our
            pool of readings and reading variants.
        """
        if len(grapheme) == 1:
            phoneme = scripts.to_hiragana(phoneme)
            readings = self._pool.get(grapheme, [])
            return phoneme in readings
        else:
            return False

    #------------------------------------------------------------------------#

    def _parse_kanjidics(self):
        """ Parses kanjidic for on and kun readings, and okurigana.
        """
        readings = {}
        reading_pool = {}
        okuri = {}

        for entry in kanjidic.Kanjidic.get_cached().itervalues():
            kanji, potential_readings, potential_okuri = \
                    self._parse_entry(entry)

            if potential_okuri:
                # not all kanji form okurigana stems
                okuri[kanji] = potential_okuri

            readings[kanji] = potential_readings

            # add pooled readings for quick checking
            pooled_readings = set()
            for reading, reading_loc, reading_type in potential_readings:
                pooled_readings.add(reading)

            rendaku_extras = filter(None, map(alternations.rendaku_variants,
                    pooled_readings))
            pooled_readings = pooled_readings.union(flatten(rendaku_extras))

            onbin_extras = filter(None, map(alternations.onbin_variants,
                    pooled_readings))
            pooled_readings = pooled_readings.union(flatten(onbin_extras))

            reading_pool[kanji] = pooled_readings

        return readings, reading_pool, okuri

    #------------------------------------------------------------------------#
    
    def _parse_entry(self, e):
        """ Parses a single line from kanjidic.
        """
        kanji = e.kanji

        readings = set()
        okurigana = set()
        for reading in e.on_readings + e.kun_readings:
            # determine the location this reading is used
            if reading.startswith('-'):
                location = ReadingLoc.suffix
                reading = reading[1:]
            elif reading.endswith('-'):
                location = ReadingLoc.prefix
                reading = reading[:-1]
            else:
                location = ReadingLoc.any

            # deterime whether it is an on or kun reading
            reading_script = scripts.script_type(reading)
            if reading_script == scripts.Script.Katakana:
                reading_type = ReadingType.on
            elif reading_script == scripts.Script.Hiragana:
                reading_type = ReadingType.kun
            else:
                # this is not an entry we want to keep
                continue

            reading = scripts.to_hiragana(reading)

            if '.' in reading:
                # the reading is a case of okurigana
                reading, okuri_ending = reading.split('.')
                # XXX threw out location and reading
                okurigana.add(okuri_ending)

            readings.add((reading, location, reading_type))

        return kanji, list(readings), list(okurigana)

    #------------------------------------------------------------------------#

    def _read_segments(self, segment_string):
        return tuple(segment_string.strip('|').split('|'))

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
