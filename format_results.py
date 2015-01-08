#!/usr/bin/python

import argparse
from collections import defaultdict
import os
import sys


class Score:
    def __init__(self, result, pos_score, neg_score):
        self.result = float(result)
        self.pos_score = float(pos_score)
        self.neg_score = float(neg_score)
    def __repr__(self):
        return "%r (%r, %r)" % (self.result, self.pos_score, self.neg_score)
    result = 0
    pos_score = 0
    neg_score = 0

def format(files):
    test_scores = defaultdict(lambda: defaultdict(Score))
    for file in files:
        scores = defaultdict(Score)
        with open(file, 'r') as r:
            next(r)
            for line in r:
                result, pos_score, neg_score, filename = line.split()
                s = Score(result, pos_score, neg_score)
                scores[filename] = s
            test_scores[file] = scores
    return test_scores

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--result-files", type=str, action="append", default=[])
    args = parser.parse_args()
    scores = format(args.result_files)
    header_string = "Model"
    first = scores.itervalues().next()
    for key in sorted(first.keys()):
        header_string += '\t%r(pos)\t%r(neg)' % (key, key)
    print header_string
    for file in args.result_files:
        output_string = file
        s = scores[file]
        for key in sorted(s.keys()):
            output_string += '\t%r\t%r' % (s[key].pos_score, s[key].neg_score)
        print output_string
        
