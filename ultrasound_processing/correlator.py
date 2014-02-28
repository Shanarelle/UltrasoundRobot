import sys
import os
import getopt
import numpy
import math

'''
	will accept two filenames.
	both will contain values of the form X,value. one value per line.
	a new sample will be delineated by START.
	the first file will contain only one sample. 
	This sample will be correlated with the samples in the other file.
	The full result will be printed for all, along with 
	a list of max correlation values for each + where they occur.
'''


def main(argv):
   matcherfile = ''
   samplefile = ''
   try:
      opts, args = getopt.getopt(argv,"m:s:",["mfile=","sfile="])
   except getopt.GetoptError:
      print 'test.py -m <matcherfile> -s <samplefile>'
      sys.exit(2)
   for opt, arg in opts:
   	if opt in ("-m", "--mfile"):
   		matcherfile = arg
   	elif opt in ("-s", "--sfile"):
   		samplefile = arg
   return matcherfile, samplefile

def cross_correlate(sample, matcher):
	correlated = numpy.correlate(sample, matcher, "full")
	normalization = sum([x**2 for x in sample])
	normalization = normalization * sum([x**2 for x in matcher])
	normalization = math.sqrt(normalization) / (len(sample) + len(matcher))
	ans = [x/normalization for x in correlated]
	return ans 


values = [[]]
correlations = []
valueIndex = -1
matcherValues = []


matcherfile, samplesfile = main(sys.argv[1:])
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
	item = int(part[2])
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
	item = int(part[2])
	matcherValues.append(item)
file.close()

#correlate each sample with the matcher
for sample in values:
	correlations.append(numpy.correlate(sample, matcherValues))

#print out results
#print repr(correlations[0])
print "max: " + repr(max(correlations[0]))
#print "max: " + repr(max(correlations[1]))