#  assertiveness
### Rules 
# 1. Direct eye contact (pupil should be captured, head movement should be consider)
# 2. Respective listening ()
# 3. Open body instance
# 4. Happy
# 5. Frowning when angry (Not copturing angry)
# 6. Covering mouth from hand (Negative)
import math
from math import *
import random

def open_body(key_cord):
    try:
        dist1 = math.hypot(key_cord[3]['x']-key_cord[7]['x'],key_cord[3]['y']-key_cord[7]['y'])
        dist2 = math.hypot(key_cord[3]['x']-key_cord[4]['x'],key_cord[3]['y']-key_cord[4]['y'])
        dist3 = math.hypot(key_cord[6]['x']-key_cord[7]['x'],key_cord[6]['y']-key_cord[7]['y'])
        dist4 = math.hypot(key_cord[6]['x']-key_cord[4]['x'],key_cord[6]['y']-key_cord[4]['y'])
        if((dist1>dist2) & (dist4>dist3)):
            return 1
    except:
        return 0
    return 0

def mouth_to_hand(key_cord):
    dist1 = 100
    dist2 = 100
    try:
        dist1 = math.hypot(key_cord[4]['x']-key_cord[0]['x'],key_cord[4]['y']-key_cord[0]['y'])    
    except:
        pass
    try:
        dist2 = math.hypot(key_cord[14]['x']-key_cord[16]['x'],key_cord[14]['y']-key_cord[16]['y'])
    except:
        pass
    return(dist1 if dist1<dist2 else dist2)

def head_movement(key_cord):
    headmovement = 0
    try:
        dist1 = math.hypot(key_cord[15]['x']-key_cord[17]['x'],key_cord[15]['y']-key_cord[17]['y'])
        dist2 = math.hypot(key_cord[14]['x']-key_cord[16]['x'],key_cord[14]['y']-key_cord[16]['y'])
        dist3 = math.hypot(key_cord[15]['x']-key_cord[1]['x'],key_cord[15]['y']-key_cord[1]['y'])
        if(dist1>dist2):
            headmovement = (dist1-dist2+dist3)/3
        else:
            headmovement = (dist2-dist1+dist3)/3
    except:
        return 0
    
    return headmovement


def assertiveness(pupil_data, key_cord, emotion):
    # print('In assertiveness: *****************')
    assertiveness = 0
    assertiveness = 40*emotion['happy']
    
    if((pupil_data['cx']!=None)):
        assertiveness = assertiveness + (int(pupil_data['cx']) + int(pupil_data['cy']))*0.60 
    
    return(abs(assertiveness) if abs(assertiveness)<100 else random.randint(85,97))
    
