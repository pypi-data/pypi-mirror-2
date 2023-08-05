# -*- coding: utf-8 -*-
# 
#  settings.py
#  gpalign
#  
#  Created by Lars Yencken on 2009-03-18.
#  Copyright 2009 Lars Yencken. All rights reserved.
# 

import os
from cjktools.common import sopen

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

class LogStream(object):
    """An output stream for logging during alignment."""
    def __init__(self, filename='align.log'):
        self.ostream = sopen(filename, 'w')
    
    def log_overconstrained(self, entry):
        print >> self.ostream, u"overconstrained: %s" % entry
    
    def log_excessive(self, entry):
        print >> self.ostream, u"excessive: %s" % entry
    
    def log_rejected(self, line):
        print >> self.ostream, u"badly formed: %s" % line
    
    @classmethod
    def get(cls):
        if not hasattr(cls, '_current'):
            cls._current = LogStream()
        
        return cls._current