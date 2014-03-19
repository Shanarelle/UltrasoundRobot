import sys
import os
import getopt
import numpy
import math
import random

'''
    Will generate 20 pseudo-random binary sequences, using a system specific source of randomness
    each sequence is of length 12
'''

sr = random.SystemRandom()
sequences = []
for index in range(20):
    sequences.append([])
    for i in range(12):
        sequences[index].append(sr.choice((0,1)))
print repr(sequences)

