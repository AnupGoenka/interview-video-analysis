#### Truthfulness 
# Rules 
# 1. Direct eye contact (Pupile + head movement)

import math
from math import *
import random

def open_body(key_cord):
    try:
        dist1 = math.hypot(key_cord[3]['x']-key_cord[7]['x'],key_cord[3]['y']-key_cord[7]['y'])
        dist2 = math.hypot(key_cord[3]['x']-key_cord[4]['x'],key_cord[3]['y']-key_cord[4]['y'])
        dist3 = math.hypot(key_cord[6]['x']-key_cord[7]['x'],key_cord[6]['y']-key_cord[7]['y'])
        dist4 = math.hypot(key_cord[6]['x']-key_cord[4]['x'],key_cord[6]['y']-key_cord[4]['y'])
        if((dist1>dist2) & (dist3>dist4)):
            return 1
    except:
        return 0
    return 0

def head_movement(key_cord):
    head_movement = 0
    try:
        dist1 = math.hypot(key_cord[15]['x']-key_cord[17]['x'],key_cord[15]['y']-key_cord[17]['y'])
        dist2 = math.hypot(key_cord[14]['x']-key_cord[16]['x'],key_cord[14]['y']-key_cord[16]['y'])
        dist3 = math.hypot(key_cord[15]['x']-key_cord[1]['x'],key_cord[15]['y']-key_cord[1]['y'])
        if(dist1>dist2):
            head_movement = (dist1-dist2+dist3)/3
        else:
            head_movement = (dist2-dist1+dist3)/3
    except:
        return 10
    
    return head_movement


def truthfulness(pupil_data, key_cord):
    # print('************ In truthfulness **************')
    truthfulness = 15
    # if(open_body(key_cord)!=1):
    #     truthfulness = truthfulness + 50
    # print('Truthfullness after openbody check: ', truthfulness)
    # truthfulness = truthfulness + 50 - head_movement(key_cord)*5
    # print('At the end of truthfulness: ', truthfulness)
    if(pupil_data['cx']!=None):
        if((pupil_data['cx']<18) & (pupil_data['cy']<18)):
            truthfulness = random.randint(70,95)
        elif((pupil_data['cx']<25) & (pupil_data['cy']<25)):
            truthfulness = random.randint(40,70)
        else:
            truthfulness = random.randint(20,50)

    return(truthfulness)
    
