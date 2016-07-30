'''
word2vec-binary-to-python-dict.py
Author: Ottokar Tilk
Author(Modified): Tony Hong
'''

# coding: utf-8
from __future__ import division

import struct
import sys
import pickle
import numpy as np

FILE_NAME = "GoogleNews-vectors-negative300.bin"
MAX_VECTORS = 37000 # This script takes a lot of RAM (>2GB for 200K vectors), if you want to use the full 3M embeddings then you probably need to insert the vectors into some kind of database
FLOAT_SIZE = 4 # 32bit float

vectors = dict()


with open('vocabulary.pcl', 'r') as f:
    result = pickle.load(f)
    words = result.keys()
    print "Length of RBE: %d" % len(words)

word_filter = dict()

for w in words:
    word_filter[w] = 1


with open(FILE_NAME, 'rb') as f:
    
    c = None
    
    # read the header
    header = ""
    while c != "\n":
        c = f.read(1)
        header += c

    total_num_vectors, vector_len = (int(x) for x in header.split())
    num_vectors = min(MAX_VECTORS, total_num_vectors)
    
    # print words

    print "Number of vectors: %d/%d" % (num_vectors, total_num_vectors)
    print "Vector size: %d" % vector_len

    while len(vectors) < num_vectors:

        word = ""        
        while True:
            c = f.read(1)
            if c == " ":
                break
            word += c

        # print word
        
        binary_vector = f.read(FLOAT_SIZE * vector_len)
        
        if word_filter.get(word, -1) == 1:
            vectors[word] = np.array([ struct.unpack_from('f', binary_vector, i)[0] 
                          for i in xrange(0, len(binary_vector), FLOAT_SIZE) ])
            sys.stdout.write("%d%%\r" % (len(vectors) / num_vectors * 100))
            sys.stdout.flush()

    print "Real length of output vectors: %d" % len(vectors)

import cPickle

print "\nSaving..."
with open(FILE_NAME[:-3] + "pcl", 'wb') as f:
    cPickle.dump(vectors, f, cPickle.HIGHEST_PROTOCOL)

