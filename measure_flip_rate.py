"""
2019-05-15 by EC
1. Initiate two command prompt window
2. First run this script in one of the command prompt (with arguments appropriate to your choice). For example, use digital pin 2, thresold 0.1, duration of measurement 5 seconds

run measure_flip_rate.py 2 0.1 5

3. Then run flip_screen.py (also with proper arguments)

The script will run for <duration> seconds then close

"""

import pyfirmata2 as pfm
#import sys
from psychopy import core
import numpy as np
import argparse
from matplotlib import pyplot as plt

def wait4change(p, thr, sflag):
    if sflag: #for initial buffer clearing
        for i in range(2000):
            val1 = p.read()
            p.board.pass_time(0.001)

            #print val1
        print("Waiting for the first flip...")

    stopflag = False
    while not stopflag:
        val1 = p.read()
        board.pass_time(0.1)
        val2 = p.read()
        #board.pass_time(0.01)

        if abs(val1 - val2) > thr:
            stopflag = True
            print("One change detected.")


try:

    #using argparse to receive arguments from command/ipython prompt
    parser = argparse.ArgumentParser() #initiate the argparse object (parser)
    parser.add_argument("INP", help="Input pin (0-3)\n") #add 1st argument
    parser.add_argument("thr", help="threshold (0 ~ 1)\n") #add 2nd argument

    parser.add_argument("duration", help="Duration of reading (positive float)\n") #add 3rd argument
    args = parser.parse_args() # call parse_args to parse the argument strings

    #assgining arguments to other variables  and convert to proper variable type
    INP = int(args.INP)
    thr = np.float(args.thr)
    duration = np.float(args.duration)


    #define the Arduino port board
    board = pfm.Arduino(pfm.Arduino.AUTODETECT)


    print("Initializing Arduino Board (%s)" % board.name)

    it = pfm.util.Iterator(board) #necessary for analog reading
    it.start() #necessary for analog reading

    p = board.analog[INP] #initiate the analog pin to read
    p.enable_reporting() #need to enable to get reading, otherwise return None

    print "Attempt to read from %s (A%d)\n" %(board.name, INP)

    c = core.Clock() #initiate a clock for timing

    #setting up numpy array to store timing and values when flip of screen occur
    samplet_rec = np.zeros(int(duration*2000)+1) #store for time
    val_rec = np.zeros(int(duration*2000)+1) #store for photo diode values
    flipt_rec = []
    k = 0 # reading counter
    j = 0 # flip counter
    #raw_input("Press enter to start measuring flips...")

    #loop until the first change in brightness deteced
    wait4change(p, thr, True)

    print("Start measuring...")

    t0 = c.getTime() #time 0
    #loop until the designate duration is reached
    tmp1 = 0
    tmp2 = 0
    while c.getTime() - t0 < duration:
        #wait4change(p, thr, False)
        #t1 = c.getTime()
        val_rec[k] = p.read()
        #print(c.getTime()-t1)
        samplet_rec[k] = c.getTime()
        #print("%.3f Change %d." %(t_rec[k], k))
        if val_rec[k] > 0.68: #brighter than higher bound
            tmp1 = val_rec[k]
        if tmp1 > 0 and val_rec[k] < 0.4: #dimmer than the lower bound
            tmp2 = val_rec[k]

        if tmp1 >0 and tmp2 > 0:
            j += 1
            tmp1 = 0
            tmp2 = 0
            flipt_rec.append(samplet_rec[k])
            print("%.3f Change %d at %d." %(samplet_rec[k], j, k))
        k += 1
        #board.pass_time(0.001)
        core.wait(.001)

        #algorithm to determine a flip
        # if val1 < val2:
        #     if (abs(val1 - val2) > thr):
        #         print("time=%.3f, (val1,val2) = %r"%(t_rec[k], val_rec[k,:]))

        t1 = c.getTime()


    print("%.3f seconds reached. %d samples taken." % (t1 - t0, k))
    print("saving data to sensordata.npz. use numpy.load to inspect.")

    samplet_rec = samplet_rec[:k]
    val_rec = val_rec[:k]

    np.savez_compressed('sensordata.npz', \
                        samplet_rec = samplet_rec, val_rec = val_rec,\
                         fc = j, flipt_rec = flipt_rec)



except KeyboardInterrupt: #to handle Ctrl + C
    print('\nUser Quit! Goodbye!')

finally:
    #if board is specified in the memory, close it
    if 'board' in dir():
        board.exit()
