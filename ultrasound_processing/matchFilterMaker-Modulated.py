''' is an EA that takes as input a file with a load of readings.
	readings will be of format : 1/0, amplitude
		where 1 means is the correct sequence
		0 means it is not and should not engender a match
	should evolve a matching algorithm that will accept the correct sequence,
	but reject all others. 

How an EA works:

1) initialise population			- all zeros

2) determine fitness				- accuracy over all samples
3) choose parents					- random
4) mutate / crossover parents		- mutate
5) choose children					- always choose the mutated child
6) iterate 2-5	
7) stop on ending condition			- end after certain number of iterations


POPULATION
- a set of values to be used as a mask
- check if set is a subset of sample to determine classification
	- want to be able to allow a certain amount of deviation (sample matches to within 10%)
		- no idea how to do that



PLAN:

load in whole file
if successive values differ, but not by much then 2 things might have occurred:
	1) is a quiet period
	2) is two sides of a peak
look at n-2 to distinguish between these two
	if difference in values more than 30% different from previous difference then its case 2
record when these occur - hopefully different for different frequencies
otherwise try looking at difference between the values (slope of line connecting the two values)
	NB. because actually a sine wave the slope will change depending on the absolute height
		hopefully two options won't overlap

	'''

import sys
import os
import random

#list of constants
SAMPLE_NUMBER = 7
TEST_NUMBER = 13
APPROXIMATION = 1
filename = "modulatorTester.txt"
test_file = "matchTesterMark3.txt"

PEAK = 1
TWO_SIDES = 2

#initialise EA variables
NUMBER_OF_ITERATIONS = 5000
POPULATION_SIZE = 40
population = [[] for i in range(POPULATION_SIZE)]

random.seed()	#initialise random number generator

'''

#for classification via sublist
def n_slices(n, list_):
    for i in xrange(len(list_) + 1 - n):
        yield list_[i:i+n]

def isSublist(list_, sub_list):
    for slice_ in n_slices(len(sub_list), list_):
        if slice_ == sub_list:
            return True
    return False

def tuple_compare(list_, sub_list):
	for index in range(len(sub_list)):
		if (sub_list[index][1] != list_[index][1]):
			return False
		if (sub_list[index][0] > list_[index][0]):
			return False
		if ((list_[index][0] - sub_list[index][0]) > 3):
			return False
	return True

def classify_sample(sampleIndex, person):
	global population
	global timing_values

	for slice_ in n_slices(len(population[person]), timing_values[sampleIndex]):
		if tuple_compare(slice_, population[person]):
			return 1
	return 0
	''
	if isSublist(timing_values[sampleIndex], population[person]):  # or hasSamePeaks(values[sampleIndex], population[person]):
		return 1
	else:
		return 0''
		

def determine_fitness_timing(person):
	global SAMPLE_NUMBER
	global classification
	fitness = 0
	answers = []
	for i in range(SAMPLE_NUMBER):
		answer = classify_sample(i, person)
		answers.append(answer)
		#print "answer: " + repr(answer) + " sampleNumber: " + repr(i)
		if answer == classification[i]:
			fitness = fitness + 1
	#print "fitness: " + repr(fitness)
	return fitness, answers

def classify_test_sample(sampleIndex, person):
	global test_timing_values

	for slice_ in n_slices(len(person), test_timing_values[sampleIndex]):
		if tuple_compare(slice_, person):
			return 1
	return 0

def determine_test_fitness_timing(person, classification):
	fitness = 0
	answers = []
	for i in range(len(classification)):
		answer = classify_test_sample(i, person)
		answers.append(answer)
		#print "answer: " + repr(answer) + " sampleNumber: " + repr(i)
		if answer == classification[i]:
			fitness = fitness + 1
	#print "fitness: " + repr(fitness)
	return fitness, answers

#do tournament selection from 3 randomly chosen individuals
def choose_parents(fitness):
	possibility1 = random.randint(0, POPULATION_SIZE-1)
	fit1 = determine_fitness_timing(possibility1)
	possibility2 = random.randint(0, POPULATION_SIZE-1)
	fit2 = determine_fitness_timing(possibility2)
	possibility3 = random.randint(0, POPULATION_SIZE-1)
	fit3 = determine_fitness_timing(possibility3)
	fitAns = max(fit1, fit2, fit3)
	if (fit1 == fitAns):
		return possibility1
	elif (fit2 == fitAns):
		return possibility2
	else:
		return possibility3


def determine_fitness_all_timing():
	global population
	fitness = []
	for i in range(POPULATION_SIZE):
		#print repr(i)
		fitness.append(determine_fitness_timing(i))
	return fitness

def mutate_timing(parent):
	global population
	#add an extra digit with 10% probability
	if random.randint(0,399) == 1:
		if (len(population[parent]) % 2 == 1):
			population[parent].append((2,0))
		else:
			population[parent].append((2,1))
	#change a digit with 20% probability
	if random.randint(0,9) == 1:
		i = random.randint(0,len(population[parent])-1)
		if i % 2 == 1:
			population[parent][i] = (random.randrange(0,40), 0)
		else:
			population[parent][i] = (random.randrange(0,40), 1)
	return parent

def initialise_timing_pop():
	global population
	#print "running initialisation"
	for person in population:
		person.append((4,1))
		person.append((2,0))
		person.append((4,1))
	#print "initialised population: " + repr(population)
	return population 	#otherwise changes are only local
	'''

#open file and fill variables with data for all iterations
def fill_file(filename):
	global APPROXIMATION
	valueIndex = -1
	classification = []
	values = []
	file = open(filename)
	for line in file:
		if line.isspace():
			continue
		if 'classification: ' in line:
			classification.append(int(line[line.find('classification: ') + 16]))
		if 'START' in line:
			valueIndex = valueIndex + 1
			values.append([])
		if ',' not in line:
			continue
		part = line.partition(',')
		if (int(part[2]) < 3200):	#if value saturated, just use previous one
			item = int(round(int(part[2]) / APPROXIMATION))
		values[valueIndex].append(item)
	file.close()
	return classification, values

# create timing based comparisons
# think about using averages to determine what counts as a peak
def create_timing_values(values):
	length = 0
	on = 0
	modulation_values = []
	for sampleIndex in range(len(values)):
		sampleList = values[sampleIndex]
		index = 2
		modulation_values.append([])
		on_amp = 50

		#print repr(midpoint) + "   " + repr(on_amp)
		for index in range(len(sampleList)):
			currentDiff = abs(sampleList[index] - sampleList[index-1])
			prevDiff = abs(sampleList[index-1] - sampleList[index-2])
			if (currentDiff > on_amp or prevDiff > on_amp):	
				if (on == 0):
					modulation_values[sampleIndex].append((0, length))
					on = 1
				if (prevDiff != 0 and ((currentDiff / prevDiff) < 1)): #check if not proper peak
					difference = abs(sampleList[index] - sampleList[index-1])
					modulation_values[sampleIndex].append((TWO_SIDES,sampleList[index],difference))
				else:
					modulation_values[sampleIndex].append((PEAK,sampleList[index]))
			else:	#if not on
				if (on == 1):
					on = 0
					length = 1
				else:					#otherwise just increment length counter
					length = length + 1
	return modulation_values

''' Main function '''

#open file and fill variables with data for one iteration
classification, values = fill_file(filename)
#print repr(values)

timing_values = create_timing_values(values)
#print "timingvalues: " + repr(timing_values)

def isNotPeak(x):
	if x[0] == TWO_SIDES:
		return True
	else:
		return False

for sample in timing_values:
	just_not_peaks = filter(isNotPeak, sample)
	list_differences = map(lambda x: x[2], just_not_peaks)
	maximum = max(list_differences)
	minimum = min(list_differences)
	average = sum(list_differences) / len(list_differences)
	print "Max: " + repr(maximum) + " Min: " + repr(minimum) + " Average: " + repr(average) + " Length: " + repr(len(list_differences))
	print repr(list_differences)

'''
#run EA using training data got from file (maybe later alternate correct and incorrect sequences)
max_fitness = 0
best_individual = []
population = initialise_timing_pop()
fitness = determine_fitness_all_timing()
for i in range(NUMBER_OF_ITERATIONS):
	parent = choose_parents(fitness)
	parent = mutate_timing(parent)
	fitness[parent] = determine_fitness_timing(parent)
	if (fitness[parent] >= max_fitness):
		max_fitness = fitness[parent]
		best_individual = population[parent]
	if ( i % 1000 == 0):
		print "\nstill running..." + repr(i)
	if (max_fitness == SAMPLE_NUMBER):
		break


#print final solution
for i in range(POPULATION_SIZE-1):
	print repr(i) + ": " + repr(population[i]) + ", fitness: " + repr(fitness[i])
print "\n\rclassifications: " + repr(classification)
print "\n\rbest seen = " + repr(max_fitness)
print "best individual = " + repr(best_individual)

#test final solution
test_classification, test_values = fill_file(test_file, test_values)
test_timing_values = create_timing_values(test_values, test_timing_values)
test_fitness = determine_test_fitness_timing(best_individual, test_classification)
print "test result: " + repr(test_fitness) + " of: " + repr(TEST_NUMBER) '''