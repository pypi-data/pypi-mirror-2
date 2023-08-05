# -*- coding: utf-8 -*-

import time
import ssc32

ssc = ssc32.SSC32('/dev/ttyUSB0', 115200,
                  autocommit=1000,
                  config='example.cfg')

# see example config.cfg
joint0 = ssc['joint0']
joint1 = ssc['joint1']
joint2 = ssc['joint2']
joint3 = ssc['joint3']
joint4 = ssc['joint4']
grip = ssc['grip']

#for i in xrange(16):
#    ssc[i].degree = 0


go_default = [(joint0, 0, 0),
              (joint1, -130, 0),
              (joint2, -45, 0),
              (joint3, 55, 0),
              (joint4, 0, 0),
              (grip, 50, 0),
             ]

def script(scr):
    """
    autocommit mode is requred
    (servo, deg, wait_time)
    """
    for move in scr:
        move[0].degree = move[1]
        while not ssc.is_done():
            time.sleep(0.01)
        time.sleep(move[2])

# initial
ssc.autocommit = 400
script(go_default)
ssc.autocommit = 1000

