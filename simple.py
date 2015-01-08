#!/usr/bin/python

import argparse
from collections import defaultdict
import math
import os
import pickle
import re
import sys
from sklearn.metrics.pairwise import cosine_similarity

from itertools import tee, izip

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def get_bigrams(filename):
    bigrams = defaultdict(int)
    file = open(filename, "r+")
    words = file.read().split()
    for v, w in pairwise(words):
        bigrams[(v, w)] += 1
    return bigrams
    

def get_features(dirs):
    file_bigrams = defaultdict(lambda: defaultdict(int))
    for d in dirs:
        for root, _, files in os.walk(d):
            for f in files:
                file_bigrams[f] = get_bigrams(os.path.join(root, f))
    return file_bigrams


def calculate_bigram_similarity(a, b):
    val = 0
    for bg, count in a.iteritems():
        if bg in b and count and b[bg]:
            #val += math.log(count + b[bg])
            val += 1
    return val


def find_similar(test_bigrams, corpus):
    max = ""
    max_val = 0
    for name, bgs in corpus.iteritems():
        val = calculate_bigram_similarity(test_bigrams, bgs)
        #print " - evaluating %s: %s" % (name, val)        
        if val > max_val:
            max_val = val
            max = name
    return max, max_val


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", type=str, action="append", default=[])
    parser.add_argument("-t", "--test", type=str, action="append", default=[])
    args = parser.parse_args()
    corpus = get_features(args.dir)
    test_features = get_features(args.test)
    for test, bigrams in test_features.iteritems():
        name, value = find_similar(bigrams, corpus)
        print "Most similar for %s (%s bigrams): %s (%s)" % (test, len(bigrams), name, value)
