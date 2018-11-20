'''
Author: Shabaz Belim Q0448 
Project : Micro expression detection for video analysis
Reference : https://www.cs.cmu.edu/~face/facs.htm,
Reference : https://en.wikipedia.org/wiki/Facial_Action_Coding_System
Reference : Naim, I., Tanveer, M.I., Gildea, D. and Hoque, E., 2016. Automated analysis and prediction of job interview performance. 
            IEEE Transactions on Affective Computing.

shape1: Neutral image
shape2: Testing
'''

import pandas as pd
import numpy as np 
from numpy import ones,vstack
from numpy.linalg import lstsq
import math
from math import *
import multiprocessing
import time
import random

def line_eq(shape, point1, point2):
    x1 = int(format(shape.part(point1)).split(',')[0][1:])
    y1 = int(format(shape.part(point1)).split(',')[1][1:-1])
    x2 = int(format(shape.part(point2)).split(',')[0][1:])
    y2 = int(format(shape.part(point2)).split(',')[1][1:-1])
#     start = time.time()
    points = [(x1,y1),(x2,y2)]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords,ones(len(x_coords))]).T
    m, c = lstsq(A, y_coords, rcond=None)[0]
    line_data = {
        'm' : m,
        'c' : c
    }
    
    return(line_data)
    


def eyebrow(shape): # outer brow height
    ######### OBH #############
    # lock = multiprocessing.Lock()
    # temp_q1 = multiprocessing.Queue()
    # lock = multiprocessing.Lock()
    # p1 = multiprocessing.Process(target=line_eq, args=(shape, 36, 39, temp_q1, lock, ))
    
    # p1.start()
    
    line_data = line_eq(shape, 36, 39)
    m = line_data['m']
    c = line_data['c']
    
    
    # p1.join()
    
    x = int(format((shape.part(17))).split(',')[0][1:])
    y = int(format((shape.part(17))).split(',')[1][1:-1])
    d1 = np.abs(y - x*m - c)
    d2 = sqrt(m**2 + 1)

    ######## IBH ###############
    x = int(format((shape.part(21))).split(',')[0][1:])
    y = int(format((shape.part(21))).split(',')[1][1:-1])
    d3 = np.abs(y - x*m - c)

    data = {
        'OBH' : d1/d2,
        'IBH' : d3/d2
    }
    # lock.acquire()
    # queue2.put(data)
    # lock.release()

    return(data)


def lips(shape):
    # lock = multiprocessing.Lock()
    # temp_q1 = multiprocessing.Queue()
    # temp_q1_lock = multiprocessing.Lock()
    # temp_q2 = multiprocessing.Queue()
    # temp_q2_lock = multiprocessing.Lock()
    # temp_q3 = multiprocessing.Queue()
    # temp_q3_lock = multiprocessing.Lock()
    # temp_q4 = multiprocessing.Queue()
    # temp_q4_lock = multiprocessing.Lock()
    ########### OLH ##########
    # p1 = multiprocessing.Process(target=line_eq, args=(shape, 50, 52, temp_q1, lock, ))
    # p2 = multiprocessing.Process(target=line_eq, args=(shape, 56, 58, temp_q2, lock, ))
    # p3 = multiprocessing.Process(target=line_eq, args=(shape, 60, 62, temp_q3, lock, ))
    # p4 = multiprocessing.Process(target=line_eq, args=(shape, 65, 63, temp_q4, lock, ))

    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()

    line_data = line_eq(shape, 50, 52)
    m1 = line_data['m']
    c1 = line_data['c']

    line_data = line_eq(shape, 56, 58)
    m2 = line_data['m']
    c2 = line_data['c']
    
    line_data = line_eq(shape, 60, 62)
    m3 = line_data['m']
    c3 = line_data['c']
    
    line_data = line_eq(shape, 65, 63)
    m4 = line_data['m']
    c4 = line_data['c']
    
    # p1.join()
    # p2.join()
    # p3.join()
    # p4.join()
    
    
    d1 =  np.abs(c2-c1)
    d2 = sqrt((((m1**2)+(m1**2))/2)+1)
    d3 =  np.abs(c3-c4)
    d4 = sqrt((((m3**2)+(m4**2))/2)+1)

    ########## LCD ##########
    m = (m1+m2+m3+m4)/4
    x1 = int(format((shape.part(48))).split(',')[0][1:])
    y1 = int(format((shape.part(48))).split(',')[1][1:-1])
    x2 = int(format((shape.part(54))).split(',')[0][1:])
    y2 = int(format((shape.part(54))).split(',')[1][1:-1])
    m5 = -(1/m)
    d5 = np.abs((y1-m*x1)-(y2-m*x2))
    d6 = sqrt(m**2+1)

    data = {
        'OLH' : d1/d2,  
        'ILH' : d3/d4,  
        'LCD' : d5/d6
    }
    # lock.acquire()
    # queue3.put(data)
    # lock.release()
    return(data)


def head_movement(key_cord):
    head_movement = 0
    dist1 = 0
    dist2 = 0
    dist3 = 0
    try:
        dist1 = math.hypot(key_cord[15]['x']-key_cord[17]['x'],key_cord[15]['y']-key_cord[17]['y'])
    except:
        pass
    try:
        dist2 = math.hypot(key_cord[14]['x']-key_cord[16]['x'],key_cord[14]['y']-key_cord[16]['y'])
    except:
        pass
    try:
        dist3 = math.hypot(key_cord[0]['x']-key_cord[1]['x'],key_cord[0]['y']-key_cord[1]['y'])
    except:
        pass
    if(dist1>dist2):
        head_movement = (dist1-dist2+dist3)/3
    else:
        head_movement = (dist2-dist1+dist3)/3
    return(head_movement*500)
    

def hand_gesture(key_cord):
    dist1 = 0
    dist2 = 0
    dist3 = 0
    dist4 = 0
    try:
        dist1 = math.hypot(key_cord[3]['x']-key_cord[7]['x'],key_cord[3]['y']-key_cord[7]['y'])
    except:
        pass
    try:
        dist2 = math.hypot(key_cord[3]['x']-key_cord[4]['x'],key_cord[3]['y']-key_cord[4]['y'])
    except:
        pass
    try:
        dist3 = math.hypot(key_cord[6]['x']-key_cord[7]['x'],key_cord[6]['y']-key_cord[7]['y'])
    except:
        pass
    try:
        dist4 = math.hypot(key_cord[6]['x']-key_cord[4]['x'],key_cord[6]['y']-key_cord[4]['y'])
    except:
        pass
    
    return(abs((dist1-dist2)-(dist3-dist4))*500)
    


def ALLemotions(shape, key_cord):
    data = {
        'eyebrow' : 0,
        'lips' : 0,
        'head_movement' : 0,
        'hand_gesture' : 0
    }
    # lock1 = multiprocessing.Lock()
    # eyebrow_queue = multiprocessing.Queue()
    # eyebrow_lock = multiprocessing.Lock()
    # lips_queue = multiprocessing.Queue()
    # lips_lock = multiprocessing.Lock()
    # head_queue = multiprocessing.Queue()
    # head_lock = multiprocessing.Lock()
    # handGesture_queue = multiprocessing.Queue()
    # handGesture_lock = multiprocessing.Lock()
    # eyebrow_p = multiprocessing.Process(target=eyebrow, args=(shape,eyebrow_queue, lock1,))
    # lips_p = multiprocessing.Process(target=lips, args=(shape, lips_queue, lock1, ))
    # head_p = multiprocessing.Process(target=head_movement, args=(key_cord, head_queue, lock1,))
    # handGesture_p = multiprocessing.Process(target=hand_gesture, args=(key_cord, handGesture_queue, lock1, ))

    eyebrow_data = eyebrow(shape)
    lips_data = lips(shape)
    # handGesture_data = hand_gesture(key_cord)
    # head_data = head_movement(key_cord)
    # eyebrow_p.start()
    # lips_p.start()
    # head_p.start()
    # handGesture_p.start()

    # eyebrow_data = eyebrow_queue.get()
    # # print('eyebrow data: ',eyebrow_data)
    # lips_data = lips_queue.get()
    # # print('lips_data :', lips_data)
    # head_data = head_queue.get()
    # # print('head data: ', head_data)
    # handGesture_data = handGesture_queue.get()
    # # print('Hand Gesture: ', handGesture_data)

    # eyebrow_p.join()
    # lips_p.join()
    # head_p.join()
    # handGesture_p.join()

    #################################################################
    ################# Distance between two ears #####################
    #################################################################
    x1 = int(format((shape.part(0))).split(',')[0][1:])
    y1 = int(format((shape.part(0))).split(',')[1][1:-2])
    x2 = int(format((shape.part(16))).split(',')[0][1:])
    y2 = int(format((shape.part(16))).split(',')[1][1:-2])

    dist_ear = math.hypot(x1-x2,y1-y2)
    b = dist_ear/480 #### 480*620 image size

    eyebrow_dist = abs((((lips_data['OLH']+lips_data['LCD'])/2)*(1/b))-69)
    lips_dist = abs((((eyebrow_data['OBH']+eyebrow_data['IBH'])/2)*(1/b))-45)*4

    try:
        data = {
            'eyebrow' : ((abs(((eyebrow_data['OBH']+eyebrow_data['IBH'])-20)/(65-20)))*100),#eyebrow_dist if eyebrow_dist<100 else random.randint(80, 100)#
            'lips' : (abs((((lips_data['OLH']+lips_data['ILH']+lips_data['LCD'])/(5))-45)/(125-45)))*100,#lips_dist if lips_dist<100 else random.randint(80,100) ## (lips_data['OLH']+lips_data['ILH']+lips_data['LCD'])/(3*5),
            'head_movement' : 0, # head_data,
            'hand_gesture' : 0 # handGesture_data
        }
    except Exception as e:
        print('some error in Allemotions: ', e)
        pass
    # print('At the end of ALLemotiondata: ', data)
    # lock.acquire()
    # emotions_queue.put(data)
    # lock.release()
    return(data)

