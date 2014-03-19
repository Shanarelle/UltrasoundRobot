import numpy
import math
import matplotlib.pyplot as plt
import random



"""
Demo of a simple plot with a custom dashed line.

A Line object's ``set_dashes`` method allows you to specify dashes with
a series of on/off lengths (in points).
""" 
def chirp():
    #parameters for the look
    plt.autoscale(False,'y')
    plt.ylim(-1.5, 1.5)
    plt.xlabel('time')
    plt.ylabel('amplitude')
    plt.suptitle('Amplitude modulated signal [1,0,1,0,0,1,0]')

    #fig = plt.figure()
    ax = plt.subplot(111)

    x = numpy.arange(300)    #[x for x in range(len(series[1]))]

    sig1 = [0, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
    sig2 = numpy.append(sig1, numpy.ones(30))
    sig = numpy.append(sig2, [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.3, 0.3, 0.3, 0.3, 0.3, 0.1, 0.1])
    notSig = numpy.zeros(15) + 0.02

    sig2 = numpy.append(sig1, numpy.ones(20))
    sigShort = numpy.append(sig2, [0.9, 0.9, 0.9, 0.9, 0.8, 0.8, 0.8, 0.8, 0.8, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.3, 0.3, 0.3, 0.3, 0.3, 0.1, 0.1])

    #construct signal pattern
    y = sigShort/3
    y = numpy.append(y, notSig)
    y = numpy.append(y, sigShort/3)
    y = numpy.append(y, notSig)
    y = numpy.append(y, notSig)
    y = numpy.append(y, notSig)
    y = numpy.append(y, sigShort/3)
    y = numpy.append(y, notSig)
    y = numpy.append(y, notSig)
    y = numpy.append(y, notSig)

    '''
    print repr(sig)
    print repr(sig1)
    print repr(sig2)
    print repr(y1[0:50])
    '''

    line, = ax.plot(x, y[x]*numpy.sin(x*0.262*4), '-', linewidth=2)

    plt.show()
    
    
def mod():
    #parameters for the look
    plt.autoscale(False,'y')
    plt.ylim(-1.5, 1.5)
    plt.xlabel('time')
    plt.ylabel('amplitude')
    plt.suptitle('Frequency modulated signal [1,0,1,0,0,1,0]')

    #fig = plt.figure()
    ax = plt.subplot(111)

    x = numpy.arange(300)    #[x for x in range(len(series[1]))]
    
    y = numpy.ones(40)*3
    y = numpy.append(y, numpy.ones(36)*2)
    y = numpy.append(y, numpy.ones(40)*3)
    y = numpy.append(y, numpy.ones(36)*2)
    y = numpy.append(y, numpy.ones(30)*2)
    y = numpy.append(y, numpy.ones(30)*2)
    y = numpy.append(y, numpy.ones(30)*2.5)
    y = numpy.append(y, numpy.ones(90)*2)
    
    line, = ax.plot(x, numpy.sin(x*0.262*y[x]), '-', linewidth=2)

    plt.show()
    
    
chirp()
    
    
    