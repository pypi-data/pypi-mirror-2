#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  param_search_align.py
#  gpalign
#  
#  Created by Lars Yencken on 2005-09-12.
#  Copyright 2005-2010 Lars Yencken. All rights reserved.
# 

import re
import os, sys
import csv
import warnings

warnings.filterwarnings("ignore")

from simplestats.aggregate import frange
from simplestats import comb

argv = sys.argv[1:]

if len(argv) < 1:
    print >> sys.stderr, 'Usage: ./param_search_align.py output.csv [extra args]'
    sys.exit(1)

output_file = argv[0]
arg_string = ' '.join(argv[1:])

total_good = re.compile('good[     ]+([0-9]+)[     ]+')

alpha_range = frange(0.1, 2.1, 0.2)
s_range = frange(0.1, 3.1, 0.2)
u_range = frange(0.1, 3.1, 0.2)

data_file = csv.writer(open(output_file, 'w'))
tmp_dir = os.tempnam('/tmp', 'param')
os.mkdir(tmp_dir)
output_file = os.path.join(tmp_dir, 'align.out')

header = ('alpha', 's', 'u', 'good')
data_file.writerow(header)
header += ('best',)
line = '%10s %10s %10s %10s %10s' % header
print line
print '-'*(len(line)+4)

best = 0
for alpha, s, u in comb.combinations(alpha_range, s_range, u_range):
    if alpha > min(u, s) or u > s:
        continue

    print '%10.2f %10.1f %10.1f' % (alpha, s, u), 
    sys.stdout.flush()
    command = './align.py %s -a %f -s %f -u %f %s' % \
            (arg_string, alpha, s, u, output_file)
    istream = os.popen(command)
    data = istream.read()

    n_good = total_good.search(data)
    if n_good is None:
        print
        print 'Having trouble with command:'
        print command
        sys.exit(1)
    else:
        n_good = int(n_good.group(1))

    if n_good > best:
        best = n_good
        print '%10d %10.2f (*)' % (n_good, best/50.0)
    else:
        print '%10d %10.2f' % (n_good, best/50.0)

    data_file.writerow((alpha, s, u, n_good))

# vim: ts=4 sw=4 sts=4 et tw=78:
