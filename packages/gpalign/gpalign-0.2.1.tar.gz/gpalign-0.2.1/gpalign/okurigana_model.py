# -*- coding: utf-8 -*-
# 
#  okurigana_model.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-09-01.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

"This module provides the OkuriganaModel class."

from os import path
import re

from cjktools import scripts, smart_cache, enum
from cjktools.common import sopen
from simplestats import sequences

from entry import Entry
from reading_model import ReadingModel
import settings

OkuriType = enum.Enum('verb', 'kanjidic', 'cooccurrence')
VerbType = enum.Enum('ichidan', 'godan', 'suru', 'irregular')

def potential_okurigana(entry):
    """ Determines whether this entry has any potential sites for
        okurigana.
    """
    assert entry.alignment, "How can an empty entry have okurigana?"
    hiragana = scripts.Script.Hiragana
    kanji = scripts.Script.Kanji

    g_segments = entry.alignment[0]

    last_segment_type = hiragana
    for i in range(len(g_segments)):
        segment_type = scripts.script_type(g_segments[i])

        if segment_type == hiragana and last_segment_type == kanji:
            # potential okurigana case
            return True

        last_segment_type = segment_type
    else:
        # exhausted this entry, no possible okurigana
        return False

#----------------------------------------------------------------------------#

def alignment_has_okurigana(g_segments, p_segments):
    """ Returns True if the given alignment has okurigana in it, False
        otherwise.
    """
    for seg in g_segments:
        if len(scripts.script_boundaries(seg)) > 1:
            return True
    else:
        return False

#----------------------------------------------------------------------------#

def remove_okurigana(g_segments, p_segments):
    """ Removes all okurigana from the segmentation.
    """
    new_g_segments = ()
    new_p_segments = ()

    i = 0
    while i < len(g_segments):
        boundaries = scripts.script_boundaries(g_segments[i])
        if len(boundaries) == 1:
            new_g_segments += (g_segments[i],)
            new_p_segments += (p_segments[i],)
            i += 1
        elif len(boundaries) == 2:
            kanji_part, kana_part = boundaries
            if i == len(g_segments)-1 or scripts.script_type(kana_part) != \
                    scripts.script_type(g_segments[i+1]):
                # last segment, or differing segments
                new_g_segments += (kanji_part, kana_part)
                new_p_segments += (p_segments[i][:-len(kana_part)],
                        p_segments[i][-len(kana_part):])
                i += 1
            else:
                # more segments, join with the next segment
                new_g_segments += (kanji_part, kana_part + g_segments[i+1])
    
                new_p_segments += (p_segments[i][:-len(kana_part)],
                        p_segments[i][-len(kana_part):] + p_segments[i+1])

                i += 2
        else:
            raise Exception, "Too many scripts per segment in %s" % g_segments

    return new_g_segments, new_p_segments

#----------------------------------------------------------------------------#

class OkuriganaModel:
    """ This class provides a verb-conjugation model for GP alignment.
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #

    def __init__(self, options):
        """ Creates a new instance by parsing edict for verb conjugation
            entries.
        """
        print "Creating a new okurigana model"
        edict_file = path.join(settings.DATA_DIR, 'edict.bz2')

        print '--> Cooccurrence threshold set to %d' % options.okuri_threshold
        self._threshold = options.okuri_threshold

        fetch_okurigana = smart_cache.disk_proxy_direct(
                self._rebuild_okurigana,
                dependencies=['okurigana_model.py', edict_file],
            )
        self._okurigana = fetch_okurigana(edict_file,
                threshold=self.threshold)

        self._evaluation_run = not bool(options.input_file)
        self._simple_mode = bool(options.simple_okurigana)

        # switches to change behaviour
        self._use_kanjidic = options.use_kanjidic
        self._use_cooccurrence = options.use_cooccurrence
        self._use_verbs = options.use_verbs

        self._n_fixed = 0

    #------------------------------------------------------------------------#

    def okurigana_adjustments(self, input_file, output_file):
        """ Reparses the entries in the given file and makes okurigana
            adjustments where necessary.
        """
        if self._evaluation_run:
            # read the evaluation input (guaranteed correctly aligned)
            entry_iter = self._evaluation_input_iter(input_file)
        else:
            # read regular input from the alignment run (may not be correctly
            # aligned)
            entry_iter = self._results_input_iter(input_file)

        ostream = sopen(output_file, 'w')

        for entry in entry_iter:
            orig_alignment = ' '.join((entry.g_string_original,
                    entry.p_string))
            if potential_okurigana:
                # potential site, attempt to solve it
                if self._simple_mode:
                    self._solve_simply(entry)
                else:
                    self._solve_okurigana(entry)

            new_alignment = entry.alignment
            
            print >> ostream, ':'.join((
                    orig_alignment,
                    ' '.join(map(lambda x: '|'.join(x), new_alignment))
                ))

        print '--> %d cases had shifted alignments' % self._n_fixed

        ostream.close()
        
    #------------------------------------------------------------------------#

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #

    def _parse_edict_entries(self, edict_file):
        """ Parses a single edict entry for a verb.
        """
        istream = sopen(edict_file)

        okurigana = {}
        counts = {}

        for line in istream:
            if not scripts.has_kanji(line):
                continue

            g_string = line.split()[0]

            # update counts for okurigana clustering
            self._update_cooccurrence(g_string, counts)

            # look for verbSpecific okurigana
            self._parse_verb_details(g_string, line, okurigana)

        istream.close()

        self._add_coccurrence_okurigana(counts, okurigana)

        return okurigana
    
    #------------------------------------------------------------------------#

    def _rebuild_okurigana(self, filename):
        okurigana_map = self._parse_edict_entries(filename)

        reading_model = ReadingModel()
        extra_okurigana = reading_model.get_okurigana()
        self._add_kanjidic_okurigana(extra_okurigana, okurigana_map)
        return okurigana_map

    #------------------------------------------------------------------------#

    def _parse_verb_details(self, g_string, line, okurigana):
        """ Determine whether this line defines a verb, and if so grab it's
            details for conjugation.
        """
        verb_tag = re.compile('\((.*,)*v(.*)\)')
        kanji_script = scripts.Script.Kanji

        tags_found = verb_tag.search(line)
        if not tags_found:
            return

        tag = tags_found.group(2)

        if tag.endswith('-s'):
            # FIXME ignore special cases for now
            return

        if tag == '1':
            verb_type = VerbType.ichidan
        elif tag.startswith('5') and len(tag) <= 2:
            verb_type = VerbType.godan
        elif tag == 's':
            verb_type = VerbType.suru
        else:
            return

        for i in range(len(g_string)-1, -1, -1):
            if scripts.script_type(g_string[i]) == kanji_script:
                last_kanji = g_string[i]
                trailing_kana = g_string[i+1:]

                if not okurigana.has_key(last_kanji):
                    okurigana[last_kanji] = set()

                okurigana[last_kanji].add((trailing_kana, OkuriType.verb, 
                        verb_type))

                break
        else:
            raise Exception, 'Error parsing grapheme string:' + `g_string`

    #------------------------------------------------------------------------#

    def _add_coccurrence_okurigana(self, counts, okurigana):
        """ Add okurigana cases based on cooccurrence, thresholded to some
            value.
        """
        kept_items = filter(lambda x: x[1] >= self._threshold, counts.items())

        counts = dict(kept_items)

        for g_string, p_string in counts.iterkeys():
            key = g_string[-1]
            okurigana.setdefault(key, set()).add(
                    (p_string, OkuriType.cooccurrence, None)
                )

    #------------------------------------------------------------------------#

    @staticmethod
    def _add_kanjidic_okurigana(kanjidic_okurigana, okurigana_map):
        """ Adds okurigana from kanjidic into the full class dictionary of
            okurigana instances.
        """
        for kanji, okurigana in kanjidic_okurigana.iteritems():
            possibleOkurigana = okurigana_map.setdefault(kanji, set())
            for case in okurigana:
                possibleOkurigana.add((case, OkuriType.kanjidic, None))

    #------------------------------------------------------------------------#

    def _add_endings(self, item, endings):
        return map(lambda x: item + x, endings)

    #------------------------------------------------------------------------#

    def _update_cooccurrence(self, g_string, counts):
        """ Updates counts for each okurigana occurence.
        """

        kanji_script = scripts.Script.Kanji
        hiragana_script = scripts.Script.Hiragana
    
        segments = list(scripts.script_boundaries(g_string))
        segments.reverse()

        last_seg = segments.pop()
        last_seg_type = scripts.script_type(last_seg)

        while segments:
            this_seg = segments.pop()
            this_seg_type = scripts.script_type(this_seg)

            if this_seg_type == hiragana_script and \
                    last_seg_type == kanji_script:
                feature = last_seg, this_seg

                counts[feature] = counts.get(feature, 0) + 1

            last_seg = this_seg
            last_seg_type = this_seg_type

        return

    #------------------------------------------------------------------------#

    def _conjugate(self, kana_ending, verb_type):
        """ Returns a list of conjugates of the verb given.
        """
        if verb_type == VerbType.ichidan:
            assert kana_ending.endswith(u'る')
            base = kana_ending[:-1]

            conjugates = self._add_endings(
                    base,
                    [u'て', u'る', u'た', u'ない', u'られる', u'られた',
                    u'られない', u'られて']
                )

            if len(kana_ending) > 1:
                conjugates.append(base)

        elif verb_type == VerbType.suru:
            if kana_ending.endswith(u'する'):
                kana_ending = kana_ending[:-2]

            conjugates = self._add_endings(
                    kana_ending,
                    [u'する', u'します', u'して', u'した', u'しない']
                )

        elif verb_type == VerbType.godan:
            last_char = kana_ending[-1]
            real_base = kana_ending[:-1]

            assert scripts.is_line(last_char, u'う')
            conjugates = [kana_ending]

            masu_base = real_base + scripts.to_line(last_char, u'い')
            conjugates.append(masu_base)
            conjugates.append(masu_base + u'ます')

            if last_char in u'いちり':
                conjugates.extend([real_base + u'って', real_base + u'った'])
            elif last_char in u'みび':
                conjugates.extend([real_base + u'んで', real_base + u'んだ'])
            elif last_char == u'き':
                conjugates.append(real_base + u'いて')
            elif last_char == u'ぎ':
                conjugates.append(real_base + u'いで')

        return conjugates

    #------------------------------------------------------------------------#

    def _evaluation_input_iter(self, filename):
        """ Provide an iterator over the evaluation input.
        """
        istream = sopen(filename, 'r')

        to_segments = lambda x: tuple(x.split('|'))

        for line in istream:
            line = line.strip()

            # we don't care about the correct entries at this stage, so just
            # get the pre-aligned input
            aligned_input, _correct_target = line.split(':')[:2]

            g_string, p_string = aligned_input.split()
            g_segments = to_segments(g_string)
            p_segments = to_segments(p_string)

            assert g_segments and p_segments

            new_entry = Entry(g_string, p_string)
            new_entry.aligned = True
            new_entry.alignment = g_segments, p_segments

            yield new_entry

        istream.close()

        return

    #------------------------------------------------------------------------#


    def _results_input_iter(self, filename):
        """ Iterates over the entries in a results file (directly output from
            the alignment script).
        """
        istream = sopen(filename, 'r')

        to_segments = lambda x: tuple(x.split('|'))

        for line in istream:
            line = line.strip()

            # although we also have the unaligned input, ignore it for now
            _unaligned_input, aligned_input = line.split(':')[:2]

            g_string, p_string = aligned_input.split()
            g_segments = to_segments(g_string)
            p_segments = to_segments(p_string)

            assert g_segments and p_segments

            new_entry = Entry(g_string, p_string)
            new_entry.aligned = True
            new_entry.alignment = g_segments, p_segments

            yield new_entry

        istream.close()

        return

    #------------------------------------------------------------------------#

    def _solve_simply(self, entry):
        """ Resolves this case by simply assuming that every site of potential
            okurigana is okurigana, and just removing all kanji->kana
            boundaries. 
        """
        hiragana = scripts.Script.Hiragana
        kanji = scripts.Script.Kanji

        g_segments = entry.alignment[0]
        i = 1
        while i < len(g_segments):
            last_segment_type = scripts.script_type(g_segments[i-1])
            segment_type = scripts.script_type(g_segments[i])

            if segment_type == hiragana and last_segment_type == kanji and \
                    g_segments[i] not in (u'の', u'が'):
                # potential okurigana case; solve then move a variable
                # increment
                i += self._shift_segments(entry, g_segments[i], i)
            else:
                i += 1

            g_segments = entry.alignment[0]

        return

    #------------------------------------------------------------------------#

    def _solve_okurigana(self, entry):
        """ Resolves this case using our full model.
        """
        hiragana = scripts.Script.Hiragana
        kanji = scripts.Script.Kanji

        g_segments = entry.alignment[0]
        i = 1
        while i < len(g_segments):
            last_segment_type = scripts.script_type(g_segments[i-1])
            segment_type = scripts.script_type(g_segments[i])

            if segment_type == hiragana and last_segment_type == kanji:
                # potential okurigana case; solve then move a variable
                # increment
                i += self._solve_single_case(entry, i)
            else:
                i += 1

            g_segments = entry.alignment[0]

        return

    #------------------------------------------------------------------------#

    def _solve_single_case(self, entry, i, default=1):
        """ A potential case of okurigana. Determine if our verb conjugation
            model solves this case.
        """
        assert entry.alignment, "We've got an empty alignment Scotty!!!"
        g_segments, p_segments = entry.alignment

        kanji_index = g_segments[i-1][-1]

        if not self._okurigana.has_key(kanji_index):
            return default

        base_okuri_options = self._okurigana[kanji_index]
        kana_options = set()
        for trailing_kana, okuri_type, sub_type in base_okuri_options:
            if okuri_type == OkuriType.verb and self._use_verbs:
                # verb okurigana
                kana_options.update(self._conjugate(trailing_kana, sub_type))
            elif okuri_type == OkuriType.kanjidic and self._use_kanjidic:
                # unknown okurigana type from kanjidic
                kana_options.add(trailing_kana)
            elif okuri_type == OkuriType.cooccurrence and \
                    self._use_cooccurrence:
                # unknown okurigana type from kanjidic
                kana_options.add(trailing_kana)
            
        # make a list of all potential matches
        potential_hits = []
        for trailing_kana in kana_options:
            if g_segments[i].startswith(trailing_kana):
                potential_hits.append((len(trailing_kana), trailing_kana))

        if potential_hits:
            # choose the longest match
            matched_kana = max(potential_hits)[1]
        elif g_segments[i] in (u'の', u'が'):
            return default
        else:
            # XXX if we can't match, just match the whole thing =)
            matched_kana = g_segments[i]

        increment = self._shift_segments(entry, matched_kana, i)

        return increment

    #------------------------------------------------------------------------#

    def _shift_segments(self, entry, kana_prefix, i):
        """ Upon finding a clear case of okurigana, this method is called to
            modify the entry.
        """
        assert entry.alignment, "Need a valid alignment to start with"
        g_segments, p_segments = entry.alignment
        self._n_fixed += 1

        shared_segments = zip(g_segments, p_segments)

        this_seg = shared_segments[i]
        last_seg = shared_segments[i-1]

        if len(this_seg[1]) == len(kana_prefix):
            # simply remove this segment boundary
            new_seg = last_seg[0] + this_seg[0], last_seg[1] + this_seg[1]

            new_segments = shared_segments[:i-1] + [new_seg] + \
                    shared_segments[i+1:]

            entry.alignment = map(tuple, sequences.unzip(new_segments))

            return 0
        else:
            # shift the segment boundary
            shiftSize = len(kana_prefix)

            (g_seg_a, g_seg_b), (p_seg_a, p_seg_b) = sequences.unzip(
                    (last_seg, this_seg))
            g_seg_a += g_seg_b[:shiftSize]
            g_seg_b = g_seg_b[shiftSize:]
            p_seg_a += p_seg_b[:shiftSize]
            p_seg_b = p_seg_b[shiftSize:]

            last_seg, this_seg = zip([g_seg_a, g_seg_b], [p_seg_a, p_seg_b])

            new_segments = shared_segments[:i-1] + [last_seg, this_seg] + \
                    shared_segments[i+1:]

            entry.alignment = map(tuple, sequences.unzip(new_segments))

            return 1

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
