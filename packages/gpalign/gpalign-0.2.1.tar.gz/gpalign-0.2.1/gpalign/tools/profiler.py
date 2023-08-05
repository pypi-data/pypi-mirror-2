#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  profiler.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-05-20.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

import segment
import profile

def test_method():
    segment.perform_segmentation('edict', 'align.out')

if __name__ == '__main__':
    profile.run('test_method()', 'profile.out')
