import sys
import os
import getopt
import numpy
import math
import matplotlib.pyplot as plt
import random

'''
	will accept two filenames.
	both will contain values of the form X,value. one value per line.
	a new sample will be delineated by START.
	the first file will contain only one sample. 
	This sample will be correlated with the samples in the other file.
	The full result will be printed for all, along with 
	a list of max correlation values for each + where they occur.
'''

"""
Demo of a simple plot with a custom dashed line.

A Line object's ``set_dashes`` method allows you to specify dashes with
a series of on/off lengths (in points).
"""
def graph_results(y_values, matcherSequence):  
    #parameters for the look
    plt.autoscale(False,'y')
    plt.xlabel('offset')
    plt.ylabel('normalized correlation')
    plt.suptitle('Correlations with respect to: ' + str(matcherSequence))
    
    #fig = plt.figure()
    ax = plt.subplot(111)
    
    for series in y_values:
        x = numpy.arange(len(series[1]))    #[x for x in range(len(series[1]))]
        line, = ax.plot(x, series[1], '--', linewidth=2, label=str(series[0]))
    #plt.acorr(y_values)

    #dashes = [10, 5, 100, 5] # 10 points on, 5 off, 100 on, 5 off
    #line.set_dashes(dashes) # means the autocorrelation one in a different style
    
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.25,
                     box.width, box.height * 0.8])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, shadow=True, ncol=2)
    #plt.ylim(-1.5, 2.0)    #think should change y axis max&min

    plt.show()
    
'''
    Will generate 20 pseudo-random binary sequences, using a system specific source of randomness
    each sequence is of length 12
'''
def generate_sequence(length, number):
    sr = random.SystemRandom()
    sequences = []
    for index in range(number):
        sequences.append([])
        for i in range(length):
            sequences[index].append(sr.choice((0,1)))
    if number == 1:
        return sequences[0]
    else:
        return sequences

def main(argv):
    matcherfile = ''
    samplefile = ''
    test = False
    try:
        opts, args = getopt.getopt(argv,"m:s:t:",["mfile=","sfile="])
    except getopt.GetoptError:
        print 'test.py -m <matcherfile> -s <samplefile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--mfile"):
            matcherfile = arg
        elif opt in ("-s", "--sfile"):
            samplefile = arg
        elif opt in ("-t"):
            test = True
    return matcherfile, samplefile, test

def cross_correlate(sample, matcher):
    correlated = numpy.correlate(sample, matcher, "same", True)
    normalization = sum([x**2 for x in sample])
    normalization2 = sum([x**2 for x in matcher])
    normalization3 = math.sqrt(normalization*normalization2)
    #print "sample: " + repr(sample)
    #print "matcher: " + repr(matcher)
    #print "before normalization: " + repr(correlated)
    ans = [x/normalization3 for x in correlated]
    #print "after normalization: " + repr(ans)
    return ans 


values = [[]]
correlations = []
valueIndex = -1
matcherValues = []


matcherfile, samplesfile, test = main(sys.argv[1:])
if (not test): #do correlation check with samples from file
    print 'Matcher file is ', matcherfile
    print 'Samples file is ', samplesfile

        #read in samples file and separate into the various samples
    file = open(samplesfile)
    for line in file:
        if line.isspace():
            continue
        if 'START' in line:
            valueIndex = valueIndex + 1
            if valueIndex != 0:
                values.append([])
        if ',' not in line:
            continue
        part = line.partition(',')
        item = float(part[2])
        values[valueIndex].append(item)
    file.close()

    #print repr(values)

    #read in matcher file
    file = open(matcherfile)
    for line in file:
        if line.isspace():
            continue
        if ',' not in line:
            continue
        part = line.partition(',')
        item = float(part[2])
        matcherValues.append(item)
    file.close()
    
    #correlate each sample with the matcher
    for sample in values:
        correlations.append((sample, cross_correlate(sample, matcherValues)))
    #autocorrelate the matcher
    correlations.append((matcherValues, cross_correlate(matcherValues, matcherValues)))
    
    graph_results(correlations, matcherValues)
else:   #generate sequences then check correlation
    #values = generate_sequence(12, 5)
    values = []
    #add new sequence
    values.append(generate_sequence(10, 1))
    #fill in sequences already in system
    values.append([1,0,0,0,1,0,0,0,0,1,0,1])
    values.append([0,0,0,0,0,0,0,1,0,0,1,0])
    values.append([1,0,1,0,0,0,1,1,1,1,1,1])
    values.append([1,1,0,1,0,0,1,1,0,0,1,0])
    values.append([0,0,0,1,0,1,0,0,1,1,0,1])
    values.append([1,1,1,0,0,0,0,0,0,1,0,1])
    values.append([1,1,0,1,1,1,0,0,0,0,0,1])
    values.append([1,1,1,1,0,1,0,1,0,1,1,1])
    values.append([0,0,1,1,1,0,1,0,0,1,0,1])
    values.append([1,0,0,0,1,1,1,0,1,0,1,0])
    
    #correlate each sample against each other, in separate graphs
    for matcher in values:
        for sample in values:
            correlations.append((sample, cross_correlate(sample, matcher)))
        graph_results(correlations, matcher)
        correlations = []


