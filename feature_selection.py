#!/usr/bin/python

import argparse
from collections import defaultdict
import math
import os
import pickle
import re
import sys


def select_features(filename):
    file = open(filename, "r+")
    # top n-grams


    # ok
    TOP = 500
    N = 4

    # sort of ok
    #TOP = 1000
    #N = 3

    # sort of ok
    #TOP = 100
    #N = 2

    # ok
    #TOP = 100
    #N = 3

    # ok
    #TOP = 500
    #N = 2

    # sort of ok
    #TOP = 50
    #N = 3

    content = file.read().lower()
    counter = defaultdict(int)
    for i in xrange(len(content)-N):
        counter[content[i:(i+N)]] += 1
    top_features = sorted(counter, key=counter.get, reverse=True)[:TOP]
    features = {k:counter[k] for k in top_features}
    return features

    # wordcount = defaultdict(int)
    # for word in file.read().split():
    #     clean_word = re.sub('[^0-9a-zA-Z]+', '', word).lower()
    #     if not len(clean_word):
    #         continue
    #     wordcount[clean_word] += 1
    # features = {k:v for k, v in wordcount.items()}
    # return features


def tfidf(feature, tf, doc_features, total_documents):
    # http://en.wikipedia.org/wiki/Tf-idf
    # tf = number of times term appears in document (parameter)
    # idf = log( total_documents / 1 + number of documents in which term appears)
    idf = math.log(total_documents / (1.0 + doc_features[feature]))
    #df = total_documents / (1 + doc_features[feature])
    if idf:
        #raise Exception("tf: %s, total_documents: %s, feature: %s, doc_features[feature]: %s" % (tf, total_documents, feature, doc_features[feature]))
        return tf / idf
    return 0.0


def print_data(dirs, all_features, type):
    unique_features = all_features['unique_features']
    doc_features = all_features['doc_features']
    total_documents = all_features['total_documents']
    for d in dirs:
        for root, _, files in os.walk(d):
            for f in files:
                features = select_features(os.path.join(root, f))
                feature_string = "%s " % type
                sorted_keys = sorted(features.keys())
                for feature in sorted_keys:
                    feature_value = features[feature]
                    if feature in unique_features:
                        feature_string += "%s:%s " % (unique_features.index(feature)+1, tfidf(feature, feature_value, doc_features, total_documents))
                        #feature_string += "%s:%s " % (unique_features.index(feature)+1, feature_value)
                print feature_string


def load_features(dirs):
    features = []
    doc_features = defaultdict(int)
    total_documents = 0
    for d in dirs:
        #print "Loading %s" % d
        for root, _, files in os.walk(d):
            for f in files:
                total_documents += 1
                selected_features = select_features(os.path.join(root, f))
                file_features = [k for k, _ in selected_features.iteritems()]
                features += file_features
                for f in file_features:
                    doc_features[f] += 1
    unique_features = set(features)
    unique_features = sorted([e for e in unique_features])
    return {"unique_features": unique_features, "doc_features": doc_features, "total_documents": total_documents}


def create_data(positive_dirs, negative_dirs, features):
    all_features = pickle.load(open(features, 'r'))
    print_data(positive_dirs, all_features, "+1")
    print_data(negative_dirs, all_features, "-1")


def create_features(feature_dirs):
    feature_dict = load_features(feature_dirs)
    pickle.dump(feature_dict, sys.stdout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--positive", type=str, action="append", default=[])
    parser.add_argument("-n", "--negative", type=str, action="append", default=[])
    parser.add_argument("-f", "--features", type=str, action="append", default=[])
    args = parser.parse_args()
    if not len(args.positive) and not len(args.negative):
        create_features(args.features)
    else:
        create_data(args.positive, args.negative, args.features[0])
