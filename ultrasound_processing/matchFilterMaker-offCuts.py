import sys
import os
import random



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
	midpoint = ((peak-trough)/2) + trough
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

	if isSublist(values[sampleIndex], population[person]):  # or hasSamePeaks(values[sampleIndex], population[person]):
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