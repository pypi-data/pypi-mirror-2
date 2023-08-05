# -*- coding: utf-8 -*-
# 
#  entry.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-08-25.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

from cjktools import scripts

class Entry:
    "A single grapheme-phoneme pair undergoing alignment."
    def __init__(self, g_string, p_string):
        self.p_string = p_string
        self.g_string_original = g_string

        # normalise the graphical form
        if u'々' in g_string:
            g_string = self._insert_duplicate_kanji(g_string)
        self.g_string = g_string

        # have we aligned yet?
        self.aligned = False

        # best alignment so far and its score
        self.score = None
        self.alignment = None

        # potential alignments and their scores
        self.potentials = None
        self.scores = None

    def __cmp__(self, rhs):
        return cmp(self.score, rhs.score)

    def __unicode__(self):
        if self.aligned:
            g_segments, p_segments = self.alignment
            s = u'Entry(%s <-> %s)' % \
                    ('|'.join(g_segments), '|'.join(p_segments))
        elif self.potentials:
            s = u'Entry(%s <-> %s, %d potentials)' % \
                    (self.g_string, self.p_string, len(self.potentials))
        else:
            s = u'Entry(%s <-> %s)' % (self.g_string, self.p_string)
        return s        

    def __str__(self):
        return unicode(self).encode('utf8')
    
    def __repr__(self):
        return str(self)

    def to_line(self):
        "Prints the final alignment in our desired output format."
        assert self.aligned

        alignment = ' '.join(map(lambda x: '|'.join(x), self.alignment))

        original = '%s %s' % (
                self.g_string_original,
                ''.join(self.alignment[1])
            )
    
        return ':'.join((original, alignment))

    def _insert_duplicate_kanji(self, g_string):
        result = []
        kanji_script = scripts.Script.Kanji
        for i, c in enumerate(g_string):
            if c == u'々' and i > 0 and \
                    scripts.script_type(g_string[i-1]) == kanji_script:
                # Insert a duplicate of the previous kanji
                result.append(g_string[i-1])
            else:
                result.append(c)

        return ''.join(result)

    def __hash__(self):
        if not self.alignment:
            return hash(self.g_string + self.p_string)
        else:
            return hash(tuple(self.alignment))

#----------------------------------------------------------------------------#
