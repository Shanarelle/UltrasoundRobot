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
APPROXIMATION = 5
filename = "matchTester.txt"

#initialise any necessary variables
values = [[] for i in range(SAMPLE_NUMBER)]
valueIndex = -1
classification = []

#initialise EA
NUMBER_OF_ITERATIONS = 15000
POPULATION_SIZE = 40
population = [[] for i in range(POPULATION_SIZE)]

random.seed()	#initialise random number generator



#for classification via sublist
def n_slices(n, list_):
    for i in xrange(len(list_) + 1 - n):
        yield list_[i:i+n]

def isSublist(list_, sub_list):
    for slice_ in n_slices(len(sub_list), list_):
        if slice_ == sub_list:
            return True
    return False

#for classification via number of peaks
def hasSamePeaks(list_, sub_list):
	trough = min(sub_list)
	peak = max(sub_list)
	midpoint = (peak-trough)/2
	noPeaks = 0
	noTroughs = 0
	for value in sub_list:		#count number of peaks in mask
		if (value > midpoint):
			noPeaks = noPeaks + 1
	for slice_ in n_slices(len(sub_list), list_):	#for each slice
		listPeaks = 0
		for value in slice_:					#count number of peaks in slice
			if (value > midpoint):
				listPeaks = listPeaks + 1
		if (noPeaks == listPeaks):				#compare with mask
			return True
		if (abs(noPeaks - listPeaks) < 3):
			return True
	return False	#no match found


#this needs to be made cleverer in due course.
#need to deal with different spaces between spikes
''' think this is the problem '''
def classify_sample(sampleIndex, person):
	global population
	global values
	#approx_person = [ round(x/50) for x in population[person] ]
	#print repr(population[person])

	if isSublist(values[sampleIndex], population[person]) or hasSamePeaks(values[sampleIndex], population[person]):
		return 1
	else:
		return 0


def determine_fitness(person):
	global SAMPLE_NUMBER
	global classification
	fitness = 0
	for i in range(SAMPLE_NUMBER):
		answer = classify_sample(i, person)
		#print "answer: " + repr(answer) + " sampleNumber: " + repr(i)
		if answer == classification[i]:
			fitness = fitness + 1
	#print "fitness: " + repr(fitness)
	return fitness


def determine_fitness_all():
	global population
	fitness = []
	for i in range(POPULATION_SIZE):
		#print repr(i)
		fitness.append(determine_fitness(i))
	return fitness

#do tournament selection from 3 randomly chosen individuals
def choose_parents(fitness):
	possibility1 = random.randint(0, POPULATION_SIZE-1)
	fit1 = determine_fitness(possibility1)
	possibility2 = random.randint(0, POPULATION_SIZE-1)
	fit2 = determine_fitness(possibility2)
	possibility3 = random.randint(0, POPULATION_SIZE-1)
	fit3 = determine_fitness(possibility3)
	fitAns = max(fit1, fit2, fit3)
	if (fit1 == fitAns):
		return possibility1
	elif (fit2 == fitAns):
		return possibility2
	else:
		return possibility3


#this also needs to get smarter
def mutate(parent):
	global population
	#add an extra digit with 10% probability
	if random.randint(0,199) == 1:
		population[parent].append(260)
	#change a digit with 20% probability
	if random.randint(0,9) == 1:
		i = random.randint(0,len(population[parent])-1)
		population[parent][i] = random.randrange(250,270)
	return parent


def initialise_pop():
	global population
	#print "running initialisation"
	for person in population:
		person.append(1300/APPROXIMATION)
		person.append(1300/APPROXIMATION)
		person.append(1300/APPROXIMATION)
	print "initialised population: " + repr(population)
	return population 	#otherwise changes are only local



#open file and fill variables with data for one iteration
file = open(filename)
for line in file:
	if line.isspace():
		continue
	if 'classification: ' in line:
		classification.append(int(line[line.find('classification: ') + 16]))
	if 'START' in line:
		valueIndex = valueIndex + 1
	if ',' not in line:
		continue
	part = line.partition(',')
	item = int(round(int(part[2]) / APPROXIMATION))
	values[valueIndex].append(item)
file.close()

print repr(values)

#run EA using training data got from file (maybe later alternate correct and incorrect sequences)
max_fitness = 0
best_individual = []
population = initialise_pop()
fitness = determine_fitness_all()
for i in range(NUMBER_OF_ITERATIONS):
	parent = choose_parents(fitness)
	parent = mutate(parent)
	fitness[parent] = determine_fitness(parent)
	if (fitness[parent] >= max_fitness):
		max_fitness = fitness[parent]
		best_individual = population[parent]
	if ( i % 1000 == 0):
		print "\nstill running..." + repr(i)


#print final solution
for i in range(POPULATION_SIZE-1):
	print repr(i) + ": " + repr(population[i]) + ", fitness: " + repr(fitness[i])
print "\n\rclassifications: " + repr(classification)
print "\n\rbest seen = " + repr(max_fitness)
print "best individual = " + repr(best_individual)
