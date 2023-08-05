# -*- coding: utf-8 -*-
# 
#  frequency.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-08-11.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

from cjktools import scripts

class FrequencyMap:
    """ The data structure within which frequency counts for tf-idf
        calculations are stored.
    """
    def __init__(self):
        self._graphemes = {}

        self._g_size = 0.0
        self._gp_size = 0.0
        self._gpc_size = 0.0
    
    def add_counts(self, alignment):
        "Increments all counts associated with the entry."
        kanji_script = scripts.Script.Kanji
        g_segments, p_segments = alignment
        for i in range(len(g_segments)):
            if scripts.script_type(g_segments[i]) == kanji_script:
                g, gp, gpc = self._get_context(g_segments, p_segments, i)

                if not self._graphemes.has_key(g):
                    # if we don't have g, we can't have gp, gpc
                    self._graphemes[g] = (1, {gp: (1, {gpc: 1})})
                    self._g_size += 1
                    self._gp_size += 1
                    self._gpc_size += 1

                else:
                    g_count, gp_dict = self._graphemes[g]
                    g_count += 1
                    if not gp_dict.has_key(gp):
                        # without gp, we also can't have gpc
                        gp_dict[gp] = (1, {gpc: 1})
                        self._gp_size += 1
                        self._gpc_size += 1
                    else:
                        gp_count, gpc_dict = gp_dict[gp]
                        gp_count += 1
                        if not gpc_dict.has_key(gpc):
                            gpc_dict[gpc] = 1
                            self._gpc_size += 1
                        else:
                            gpc_dict[gpc] += 1
                        gp_dict[gp] = gp_count, gpc_dict
                    self._graphemes[g] = g_count, gp_dict
    
    def del_counts(self, alignment):
        "Decrements all counts associated with the entry."
        kanji_script = scripts.Script.Kanji
        g_segments, p_segments = alignment
        for i in range(len(g_segments)):
            if scripts.script_type(g_segments[i]) == kanji_script:
                g, gp, gpc = self._get_context(g_segments, p_segments, i)
                g_count, gp_dict = self._graphemes[g]
                g_count -= 1
                if g_count < 1:
                    del self._graphemes[g]
                    self._g_size -= 1
                    continue

                gp_count, gpc_dict = gp_dict[gp]
                gp_count -= 1
                if gp_count < 1:
                    del gp_dict[gp]
                    self._gp_size -= 1
                    self._graphemes[g] = g_count, gp_dict
                    continue

                gpcCount = gpc_dict[gpc]
                gpcCount -= 1
                if gpcCount < 1:
                    del gpc_dict[gpc]
                    self._gpc_size -= 1
                else:
                    gpc_dict[gpc] = gpcCount

                gp_dict[gp] = gp_count, gpc_dict
                self._graphemes[g] = g_count, gp_dict

        return
        
    def _get_context(self, g_segments, p_segments, index):
        """
        Determine the context needed for calculations or for frequency 
        updates.
        """
        grapheme = g_segments[index]
        phoneme = p_segments[index]

        # determine the left context...
        if index > 0:
            leftG = g_segments[index-1]
            leftP = p_segments[index-1]
        else:
            leftG = None
            leftP = None

        # ...and the right context 
        if index < len(g_segments) - 1:
            rightG = g_segments[index+1]
            rightP = p_segments[index+1]
        else:
            rightG = None
            rightP = None

        return grapheme, phoneme, (leftG, leftP, rightG, rightP)
    
    def frequencies(self, g_segments, p_segments, index):
        """
        Calculates the frequencies of occurence of the segment specified
        within the alignment.
        """
        g, gp, gpc = self._get_context(g_segments, p_segments, index)

        g_freq, gp_dict = self._graphemes.get(g, (0, {}))
        gp_freq, gpc_dict = gp_dict.get(gp, (0, {}))
        gpc_freq = gpc_dict.get(gpc, 0)

        g_freq /= self._g_size
        gp_freq /= self._gp_size
        gpc_freq /= self._gpc_size

        return g_freq, gp_freq, gpc_freq
    
#----------------------------------------------------------------------------#
