#### Curiosity
# Rules
# 1. Head upward | intrested
# 2. Head down  | Not intrsted
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
        return 10
    
    return head_movement

def curiosity(pupil_data, key_cord):
    # print('********** In curiousity ************')
    curiosity = 0
    if(pupil_data['cx']!=None):
        curiosity = curiosity + (int(pupil_data['cx'])+int(pupil_data['cy']))*0.5 + int(pupil_data['radius'])*0.01
    # temp =  head_movement(key_cord)
    # print('head movement in curiosity:', temp)
    # curiosity = curiosity + 50 - (temp*5)
    # print('At the end of curiosity: ', curiosity)
    return(abs(curiosity) if abs(curiosity) <100 else random.randint(80,95))
    

