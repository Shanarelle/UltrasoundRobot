import sys
import getopt
import numpy
import math
import matplotlib.pyplot as plt

"""
Demo of a simple plot with a custom dashed line.

A Line object's ``set_dashes`` method allows you to specify dashes with
a series of on/off lengths (in points).
"""

def graph_results(y_values, title, labels):  
    #parameters for the look
    #plt.autoscale(False,'y')
    plt.xlabel('time')
    plt.ylabel('amplitude')
    plt.suptitle(title)
    
    #fig = plt.figure()
    ax = plt.subplot(111)
    
    lineCount = 0
    
    for series in y_values:
        x = numpy.arange(len(series))
        line, = ax.plot(x, series, '-', linewidth=2, label=str(labels[lineCount]))      #, drawstyle='steps-mid'

        if lineCount > 6:
            dashes = [10, 5, 20, 5] # 10 points on, 5 off, 100 on, 5 off
            line.set_dashes(dashes) # means the later ones in a different style
        lineCount = lineCount + 1
    #plt.acorr(y_values)
    
    '''
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.25,
                     box.width, box.height * 0.8])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, shadow=True, ncol=2)
    #plt.ylim(-1.5, 2.0)    #think should change y axis max&min
    '''

    plt.show()
   
    
    
def main(argv):
    matcherfile = ''
    samplefile = ''
    number = ''
    test = False
    try:
        opts, args = getopt.getopt(argv,"s:n:")
    except getopt.GetoptError:
        print 'test.py -s <samplefile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s"):
            samplefile = arg
        elif opt in ("-n"):
            number = arg
    return samplefile, number
    
    
    

values = [[]]
valueIndex = -1

samplesfile, number = main(sys.argv[1:])

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

print repr(values) '''
TWO_PI = 6.284
amplitude = 0.5
values = []
values.append([])
for x in range(2):
    for time in range(20):
        intermediary = (TWO_PI / 20) * (time+15)
        intermediary2 = amplitude * numpy.sin(intermediary)
        values[0].append(intermediary2 + amplitude)
'''
graph_results(values, "Optimal vs Transmitted Sine Wave", ["Actual"])