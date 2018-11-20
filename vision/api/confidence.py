### Chin up
### Open/Close body 
### eye contact 
### head_movement
import math 
from math import *
import random

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
        return 6
    
    return head_movement

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

def confidence(key_cord, pupil_data, emotion):
    # print('************ In confidence ****************')
    confidence = 0
    if(emotion['happy']>0):
        confidence = 35*emotion['happy']
    # if(open_body(key_cord)==1):
    #     confidence = confidence + 15
    # confidence = confidence + 30 - head_movement(key_cord)*5
    if(pupil_data['cx']!=None):
        confidence = confidence + (int(pupil_data['cx'])+int(pupil_data['cy']))*0.30 + int(pupil_data['radius'])*0.002
    # print('At the end of confidence: ', confidence)
    return(confidence if confidence<100 else random.randint(80,100))
    