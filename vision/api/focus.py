### pupil detection 
### head movement
### open body 
### happy negative
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

def focus(pupil_data, emotion_data, key_cord):
    focus = 0
    focus = focus - emotion_data['happy']*100 + emotion_data['surprise']*100+ emotion_data['neutral']*100
    if(pupil_data['cx']!=None):
        focus = focus + (int(pupil_data['cx'])+int(pupil_data['cy']))*0.45
    return (abs(focus) if abs(focus)< 85 else random.randint(80,95))
    # print('In focus key_cord: ', key_cord)
    # temp = head_movement(key_cord)
    # print('head movement in focus: ', temp)
    # focus = focus + 50 - (5*temp)
    # print('focus in focus: ', focus)
    # if(open_body(key_cord)==0):
        # focus = focus + 20

    
    
    
    