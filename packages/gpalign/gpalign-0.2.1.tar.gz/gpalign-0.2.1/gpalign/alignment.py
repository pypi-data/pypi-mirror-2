# -*- coding: utf-8 -*-
# 
#  alignment.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-05-16.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

"This module implements the iterative TF-IDF alignment method."

import os
import math
import random
import cPickle as pickle

from cjktools import scripts
from cjktools.common import sopen
from consoleLog.progressBar import ProgressBar
from consoleLog import default as _log

import potentials
from frequency import FrequencyMap

# epsilon for testing for zero
eps = 1e-8

class AlignmentModel:
    """ This class is responsible for the alignment algorithm, and all its
        internal data structures.
    """
    def __init__(self, output_file, options):
        """ Creates a new instance using the list of correctly aligned
            readings.
        """
        _log.start('Initialising alignment model')
        if options.model_input:
            _log.log('Seeding from %s' %  
                    os.path.basename(options.model_input))
            self._unique_counts = pickle.load(open(options.model_input))
        else:
            _log.log('Seeding from empty model')
            self._unique_counts = FrequencyMap()

        self._ambiguous_counts = FrequencyMap()

        # possibly a filename to dump our final model into
        self._model_dump_file = options.model_output

        # whether to align all at once or iteratively
        self._iterative = options.iterative

        # we write aligned readings as we go, rather than storing them in
        # memory
        self._output = sopen(output_file, 'w')
        self._output_name = output_file

        # ratios for the tf-idf
        self._alpha = options.alpha
        self._solved = options.solved
        self._unsolved = options.unsolved

        # setting either of these defaults non-zero will prevent calculation
        # of that heuristic
        if options.random:
            self._use_random = True
            _log.log('Random model selected')
        else:
            self._use_random = False

            # only define these variables in the non-random case to ensure
            # that they never get used in the random case
            self._default_tf = 0
            self._default_idf = 0
    
            if not options.tf_heuristic:
                _log.finish('Disabling tf heuristic')
                self._default_tf = 1
    
            elif not options.idf_heuristic:
                _log.finish('Disabling idf heuristic')
                self._default_idf = 1
            
            else:
                _log.finish('Full TF-IDF enabled')
    
    #------------------------------------------------------------------------#

    def add_resolved(self, resolved_entries):
        """ Populates the statistical model with a number of resolved entries. 
        """
        # add all unambiguous readings to our model
        for entry in resolved_entries:
            self._unique_counts.add_counts(entry.alignment)
            print >> self._output, entry.to_line()

    #------------------------------------------------------------------------#

    def disambiguate(self, ambiguous):
        """ Incorporates and aligns the ambiguous readings based on existing
            alignments.
        """
        if not ambiguous:
            return

        self._initialise_entries(ambiguous)
        num_entries = len(ambiguous)

        if self._use_random:
            # randomly pick the best alignment for each entry
            self._random_alignment(ambiguous)

        elif not self._iterative:
            # perform first and only scoring iteration
            self._rescore(ambiguous)
    
        progress_bar = ProgressBar()
        progress_bar.start(100)

        i = 0
        while i < num_entries:
            if self._iterative and not self._use_random:
                # perform expensive rescoring
                self._rescore(ambiguous)
                ambiguous.sort()

            best_entry = ambiguous.pop()
            self._disambiguate_entry(best_entry)

            print >> self._output, best_entry.to_line()

            i += 1
            progress_bar.fractional(math.sqrt(i)/math.sqrt(num_entries))

        progress_bar.finish()

    #------------------------------------------------------------------------#
    
    def finish(self):
        """ Closes the output stream and sorts the output for easier
            comparison.
        """
        self._output.close()

        if self._model_dump_file:
            # dump our 
            ostream = open(self._model_dump_file, 'w')
            pickle.dump(self._unique_counts, ostream)
            ostream.close()

        assert self._ambiguous_counts._g_size == 0
    
    #------------------------------------------------------------------------#

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #

    def _initialise_entries(self, ambiguous_entries):
        """ Updates the counts for ambiguous readings and restructures them to
            be updated.
        """
        for i in xrange(len(ambiguous_entries)):
            entry = ambiguous_entries[i]
            alignments = entry.potentials

            assert len(set(alignments)) == len(alignments), \
                    "Readings are not unique"

            # update our counts
            for alignment in alignments:
                self._ambiguous_counts.add_counts(alignment)

            entry.score = 0.0
            entry.scores = [0.0]*len(alignments)
 
    #------------------------------------------------------------------------#

    def _disambiguate_entry(self, entry):
        """ Modify the entry to remove all the additional ambiguous
            alignments, and update our internal counts.
        """
        entry.scores = None

        # put this count amongst the unique ones
        self._unique_counts.add_counts(entry.alignment)

        # fill in the rest of this count
        # eliminate the bad readings from the model
        for alignment in entry.potentials:
            self._ambiguous_counts.del_counts(alignment)

        entry.potentials = None
        entry.aligned = True

    #------------------------------------------------------------------------#

    def _rescore(self, ambiguous):
        """ Loops over the entire list of ambiguous entries, rescoring each.
        """
        for i in xrange(len(ambiguous)):
            entry = ambiguous[i]

            entry.scores = map(self._tfidf, entry.potentials)
            entry.score, entry.alignment = max(zip(entry.scores, \
                    entry.potentials))

    #------------------------------------------------------------------------#

    def _weighted_freqs(self, g_segments, p_segments, index):
        """ Weight the frequencies from the two models.
        """
        s_g_freq, s_gp_freq, s_gpc_freq = self._unique_counts.frequencies(
                g_segments, p_segments, index)
        u_g_freq, u_gp_freq, u_gpc_freq = self._ambiguous_counts.frequencies(
                g_segments, p_segments, index)

        g_freq = self._solved*s_g_freq + self._unsolved*u_g_freq
        gp_freq = self._solved*s_gp_freq + self._unsolved*u_gp_freq
        gpc_freq = self._solved*s_gpc_freq + self._unsolved*u_gpc_freq

        return g_freq, gp_freq, gpc_freq
        
    #------------------------------------------------------------------------#

    def _explain_alignment(self, entry, alignment):
        """
        """
        best_score, all_alignments = entry
        print '--->', best_score,
        potentials.print_alignment(alignment)
        all_alignments.sort()
        all_alignments.reverse()
        for other_score, other_alignment in all_alignments:
            print '----->', other_score,
            potentials.print_alignment(other_alignment)
    
    #------------------------------------------------------------------------#

    def _random_alignment(self, entries):
        """ Picks a random alignment for each entry in a list of ambiguous
            entries. 
        """
        for ambiguous_entry in entries:
            ambiguous_entry.alignment = random.sample(
                    ambiguous_entry.potentials, 1)[0]

    #------------------------------------------------------------------------#

    def _tfidf(self, alignment):
        """ Calculates the tf-idf score of the alignment passed in based on
            the current model.
        """
        kanji_script = scripts.Script.Kanji
        current_scores = []

        g_segments, p_segments = alignment
        for i in range(len(g_segments)):
            if not scripts.script_type(g_segments[i]) == kanji_script:
                continue

            g_freq, gp_freq, gpc_freq = self._weighted_freqs(g_segments,
                    p_segments, i)

            tf = self._default_tf or \
                (gp_freq + self._alpha - self._unsolved) / g_freq

            idf = self._default_idf or \
                math.log(gp_freq/(gpc_freq + self._alpha - self._unsolved))

            current_scores.append(tf*idf)
 
        new_score = sum(current_scores) / float(len(current_scores))

        return new_score

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

