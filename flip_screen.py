"""
2019-05-21 by EC
flash the screen in desired rate (but within the capacity of your display, usually max = 60 Hz)
#run this script once measure_flip_rate.py is ready


"""
from psychopy import visual, core, event
import sys
import numpy as np
import argparse

def boolean_string(s):
    """
        for converting the --fsflag in arguments into boolean
    """
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'


def waitkey(c, period):
    """
        a function to wait key press for period seconds
    """
    t0 = c.getTime()
    key = event.getKeys()
    while c.getTime() - t0 < period:
        key = event.getKeys()
        if len(key) >0:
            if key[0] == 'escape':
                print("User quit!\n")
                core.quit()


try:
    #a more informative way of defining arguments than sys.argv
    parser = argparse.ArgumentParser()
    parser.add_argument("rate", help="Frequency of the flipping\n")
    parser.add_argument("duration", help="duration of flipping screen\n")
    parser.add_argument("fsflag", type =  boolean_string,
                        help="fullscr flag (True/False)\n")

    args = parser.parse_args()


    rate = np.float(args.rate)
    duration = np.float(args.duration)
    fsflag = args.fsflag
    #end of variable assignment



    win = visual.Window(color = (-1,-1,-1),
                        pos=(-100,200),
                        fullscr = fsflag)
    mou = event.Mouse(visible=False)
    txt = visual.TextStim(win, text = "Attach sensor to screen. hit enter to start flickering when ready...")
    period = 1/rate #period in seconds
    halfperiod = 0.5 * period #compute half of the period (divide a period into dark and bright)
    c = core.Clock()
    txt.draw()
    win.flip()
    event.waitKeys(keyList=["return"])
    t0 = c.getTime()

    while c.getTime() - t0 < duration:
        win.color = (1,1,1) #turn window to white
        win.callOnFlip(waitkey, c, halfperiod) #call waitkey right after flip
        win.flip()

        win.color = (-1,-1,-1) #turn window to black
        win.callOnFlip(waitkey, c, halfperiod) #call waitkey right after flip
        win.flip()
    win.color = (-1, -1, -1)
    win.flip()


    print("\n total duration: %.3f seconds " % (c.getTime() - t0))


except KeyboardInterrupt:
    print("User Quit!\n")

finally:
    mou.setVisible(1)
    win.close()
