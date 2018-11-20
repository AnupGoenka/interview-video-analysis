#### TO kill multiple process=> kill -9 $(ps -aux | grep 8000|awk -F" " {'print $2'})
#### sudo lsof -i:8080
import glob
import math
import multiprocessing
import os
import pickle
import sys
from json import dumps
from math import *

import cv2
import numpy as np
import pandas as pd

import dlib
from vision import BASE_DIR, PROJECT_ID, TOPIC_NAME, publisher, topic_name
from vision.api.assertiveness import assertiveness
from vision.api.confidence import confidence
from vision.api.curiosity import curiosity
from vision.api.energy import energy
from vision.api.focus import focus
from vision.api.MicroExpresssion import ALLemotions
from vision.api.pupil import pupil
# from vision.api.run import main_fun
from vision.api.truthfulness import truthfulness

predictor = None
detector = None
clf = None
neutral_shape = None

final_emotions_data = {
    'happy': 0,
    'neutral': 0,
    'sadness': 0,
    'surprise': 0,
    'eyebrow': 0,
    'lips': 0,
    'head_movement': 0,
    'hand_gesture': 0,
    'confidence': 0,
    'energy': 0,
    'truthfulness': 0,
    'curiosity': 0,
    'assertiveness': 0
}
neutral_emotion_data = final_emotions_data

emotions_data = {
        'happy' : 0,
        'neutral' : 0,
        'sadness' : 0,
        'surprise' : 0
        }

def publish_data(redisKey, user_id, redis_data): 
    try:
        publisher.publish(topic_name, dumps(redis_data).encode(), user_id=user_id, key=redisKey)
    except Exception as e:
        print("Failed to publish data : ", e)

# publish_data("test", 'asdasd', "YOLO")

# def prediction_int(x_test, pred_int, lock):
#     global clf
#     try:
#         pred = clf.predict(x_test)
#     except:
#         pred = []
#         pred.append(5)
#     lock.acquire()
#     pred_int.put(pred)
#     lock.release()


def prediction_prob(x_test):
    global clf
    try:
        pred = clf.predict_proba(x_test)
        return(pred)

    except Exception as e:
        pred = [[0,0,0,0]]
        return(pred)

def get_landmarks(image, q, lock):
    global predictor
    global detector
    shape = None

    data = []

    emotions_data = {
        'happy': 0,
        'neutral': 0,
        'sadness': 0,
        'surprise': 0
    }

    detector = dlib.get_frontal_face_detector()
    detections = detector(image, 1)

    for k, d in enumerate(detections):
        shape = predictor(image, d)
        xlist = []
        ylist = []
        for i in range(1, 68):
            xlist.append(float(shape.part(i).x))
            ylist.append(float(shape.part(i).y))
        xmean = np.mean(xlist)
        ymean = np.mean(ylist)
        xcentral = [(x - xmean) for x in xlist]
        ycentral = [(y - ymean) for y in ylist]
        landmarks_vectorised = []
        for x, y, w, z in zip(xcentral, ycentral, xlist, ylist):
            landmarks_vectorised.append(w)
            landmarks_vectorised.append(z)
            meannp = np.asarray((ymean, xmean))
            coornp = np.asarray((z, w))
            dist = np.linalg.norm(coornp - meannp)
            landmarks_vectorised.append(dist)
            landmarks_vectorised.append((math.atan2(y, x) * 360) / (2 * math.pi))
        data = landmarks_vectorised
    if len(detections) >= 1:
        X_test = np.array(data)
        X_test = np.reshape(X_test, (1, -1))
        if (shape != None):
            # pred_int = multiprocessing.Queue()
            # pred_proba = multiprocessing.Queue()

            # p1 = multiprocessing.Process(target=prediction_int, args=(X_test, pred_int,lock, ))
            # p2 = multiprocessing.Process(target=prediction_prob, args=(X_test, pred_proba,lock, ))

            # p1.start()
            # p2.start()

            # pred = pred_int.get()
            # pred_prob = pred_proba.get()

            # p1.join()
            # p2.join()

            pred_prob = prediction_prob(X_test)

            pred_prob = pred_prob[0]
            # random_value = random.randint(30,200)/100
            # temp_value = float(pred_prob[1])/(float(pred_prob[0]) + float(pred_prob[2]) + float(pred_prob[3]))
            emotions_data['happy'] = float(pred_prob[0]) #+ temp_value*float(pred_prob[0]) 
            emotions_data['surprise'] = float(pred_prob[3]) #+ temp_value*float(pred_prob[3]) 
            emotions_data['sadness'] = float(pred_prob[2]) #+ temp_value*float(pred_prob[2]) + random_value
            #emotions_data['neutral'] = float(pred_prob[1])
    lock.acquire()
    q.put(emotions_data)
    q.put(shape)
    lock.release()

def emotions(filepath, filename):
    global predictor
    global clf
    global neutral_emotion_data
    global emotions_data
    micro_expression_data = {}
    success = os.path.isfile(filepath +filename)
    lock = multiprocessing.Lock()

    while (success == True):
        data_queue = multiprocessing.Queue()
        # pose_queue = multiprocessing.Queue()
        pupil_queue = multiprocessing.Queue()
        image1 = cv2.imread(filepath + filename, 0)
        land_p = multiprocessing.Process(target=get_landmarks, args=(image1, data_queue, lock, ))
        # pose_p = multiprocessing.Process(target=main_fun, args=(filepath+filename, pose_queue, lock, ))
        pupil_p = multiprocessing.Process(target=pupil, args=(image1, pupil_queue,lock, ))

        pupil_p.start()
        land_p.start()
        # pose_p.start()

        pupil_data = pupil_queue.get()
        # print('pupil_data: ', pupil_data)
        emotions_data = data_queue.get()
        # print('emotions_data: ', emotions_data)
        shape = data_queue.get()
        # print('shape: ', shape)
        # key_cord = pose_queue.get()
        key_cord = None
        # print('key_cord: ', key_cord)

        land_p.join()
        # pose_p.join()
        pupil_p.join()

        if (shape != None):
            # emotions_queue = multiprocessing.Queue()
            # confidence_queue = multiprocessing.Queue()
            # energy_queue = multiprocessing.Queue()
            # assertiveness_queue = multiprocessing.Queue()
            # truthfulness_queue = multiprocessing.Queue()
            # curiosity_queue = multiprocessing.Queue()
            # focus_queue = multiprocessing.Queue()

            # micro_expression_p = multiprocessing.Process(target=ALLemotions, args=(shape, key_cord, emotions_queue,lock,))
            # confidence_p = multiprocessing.Process(target=confidence,
            #                                        args=(key_cord, pupil_data, emotions_data, confidence_queue,lock,))
            # energy_p = multiprocessing.Process(target=energy,
            #                                    args=(key_cord, pupil_data, emotions_data, shape, energy_queue,lock,))
            # assertiveness_p = multiprocessing.Process(target=assertiveness,
            #                                           args=(pupil_data, key_cord, emotions_data, assertiveness_queue,lock,))
            # truthfullness_p = multiprocessing.Process(target=truthfulness,
            #                                           args=(pupil_data, key_cord, truthfulness_queue,lock,))
            # curiosity_p = multiprocessing.Process(target=curiosity, args=(pupil_data, key_cord, curiosity_queue,lock,))
            # focus_p = multiprocessing.Process(target=focus, args=(pupil_data, emotions_data, key_cord, focus_queue, lock, ))

            # micro_expression_p.start()
            # confidence_p.start()
            # energy_p.start()
            # assertiveness_p.start()
            # truthfullness_p.start()
            # curiosity_p.start()
            # focus_p.start()

            # confidence_data = confidence_queue.get()
            # # print('confidence: ', confidence_data)
            # micro_expression_data = emotions_queue.get()
            # # print('micro_expression_data: ', micro_expression_data)
            # energy_data = energy_queue.get()
            # # print('energy_data:', energy_data)
            # assertiveness_data = assertiveness_queue.get()
            # # print('assertiveness_data: ', assertiveness_data)
            # truthfulness_data = truthfulness_queue.get()
            # # print('truthfulness_data: ', truthfulness_data)
            # curiosity_data = curiosity_queue.get()
            # # print('curiosity_data: ', curiosity_data)
            # focus_data = focus_queue.get()
            # print('focus data: ',focus_data )

            # micro_expression_p.join()
            # confidence_p.join()
            # energy_p.join()
            # assertiveness_p.join()
            # truthfullness_p.join()
            # curiosity_p.join()
            # focus_p.join()

            micro_expression_data = ALLemotions(shape, key_cord)
            confidence_data = confidence(key_cord, pupil_data, emotions_data)
            energy_data = energy(key_cord, pupil_data, emotions_data, shape)
            assertiveness_data = assertiveness(pupil_data, key_cord, emotions_data)
            truthfulness_data = truthfulness(pupil_data, key_cord)
            curiosity_data = curiosity(pupil_data, key_cord)
            focus_data = focus(pupil_data, emotions_data, key_cord)


        success = False

    try:
        final_emotions_data = {
            'happy': emotions_data['happy'],
            'neutral': emotions_data['neutral'],
            'sadness': emotions_data['sadness'],
            'surprise': emotions_data['surprise'],
            'eyebrow': abs(micro_expression_data['eyebrow']),
            'lips': abs(micro_expression_data['lips']),
            'head_movement': abs(micro_expression_data['head_movement']),
            'hand_gesture': abs(micro_expression_data['hand_gesture']),
            'confidence': confidence_data,
            'energy': energy_data,
            'assertiveness': assertiveness_data,
            'truthfulness': truthfulness_data,
            'curiosity': curiosity_data,
            'focus' : focus_data
        }
    except Exception as e:
        final_emotions_data = {
            'happy': 0,
            'neutral': 0,
            'sadness': 0,
            'surprise': 0,
            'eyebrow': 0,
            'lips': 0,
            'head_movement': 0,
            'hand_gesture': 0,
            'confidence': 0,
            'energy': 0,
            'truthfulness': 0,
            'curiosity': 0,
            'assertiveness': 0,
            'focus' : 0
        }

    
    return final_emotions_data


def video_analysis(filename, filepath, redisKey, userId, count):
    global predictor
    global clf
    global neutral_emotion_data
    
    # predictor_path = '-f'
    # faces_folder_path = '/run/user/1004/jupyter/kernel-7ac3ad8c-5727-435a-91b0-b93e35ef293b.json'
    # detector = dlib.get_frontal_face_detector()
    if (predictor == None):
        predictor = dlib.shape_predictor(BASE_DIR + '/vision/api/shape_predictor_68_face_landmarks.dat')

    print("#########################################")
    final_emotions_data = emotions(filepath, filename)
    # firstimage = 'firstimage/'
    # os.system('sudo cp -rf %s%s'%(filepath, firstimage))
    print("DELETING LOCAL FILE")
    # os.remove(filepath + filename)
    print("DELETED LOCAL FILE")

    try:
        emotion_data = {
            'traits': {
                'Confidence': int(final_emotions_data['confidence']),
                'Energy': int(final_emotions_data['energy']),
                'Assertiveness': int(final_emotions_data['assertiveness']),
                'Trust': int(final_emotions_data['truthfulness']),
                'Curiosity': int(final_emotions_data['curiosity']),
                'Focus': int(final_emotions_data['focus'])
            },
            'happy': final_emotions_data['happy'],
            'neutral': final_emotions_data['neutral'],
            'sadness': final_emotions_data['sadness'],
            'surprise': final_emotions_data['surprise'],
            'eyebrow': abs(final_emotions_data['eyebrow'] - neutral_emotion_data['eyebrow']),
            'lips': abs(final_emotions_data['lips'] - neutral_emotion_data['lips']),
            'head_movement': abs(final_emotions_data['head_movement'] - neutral_emotion_data['head_movement']),
            'hand_gesture': abs(final_emotions_data['hand_gesture'] - neutral_emotion_data['hand_gesture'])
        }

    except Exception as e:
        print('you dont have good file format and ',e)
        emotion_data = {
            'traits': {
                'Confidence': neutral_emotion_data['confidence'],
                'Energy': neutral_emotion_data['energy'],
                'Assertiveness': neutral_emotion_data['assertiveness'],
                'Trust': neutral_emotion_data['truthfulness'],
                'Curiosity': neutral_emotion_data['curiosity'],
                'Focus': 0
            },
            'happy': neutral_emotion_data['happy'],
            'neutral': neutral_emotion_data['neutral'],
            'sadness': neutral_emotion_data['sadness'],
            'surprise': neutral_emotion_data['surprise'],
            'eyebrow': abs(neutral_emotion_data['eyebrow'] - neutral_emotion_data['eyebrow']),
            'lips': abs(neutral_emotion_data['lips'] - neutral_emotion_data['lips']),
            'head_movement': abs(neutral_emotion_data['head_movement'] - neutral_emotion_data['head_movement']),
            'hand_gesture': abs(neutral_emotion_data['hand_gesture'] - neutral_emotion_data['hand_gesture'])
        }

    try:
        redis_data = {
            'count': count,
            'data': emotion_data
        }
        publish_data(redisKey, userId, redis_data) ### Should uncomment on production ######
        # redis_conn.rpush(redisKey, dumps(redis_data))
        # redis_conn.expire(redisKey, 60 * 60 *24)
    except Exception as e:
        print("In redis exception {}".format(str(e)))
    print('Final emotions data after substraction: ', emotion_data)
    return emotion_data


def VIA(filename, filepath, redisKey, userId, count):
    global clf
    if (clf == None):
        clf = pickle.load(open(BASE_DIR + '/vision/api/xgb_model1.sav', 'rb'))
    return_data = video_analysis(filename, filepath, redisKey, userId, count)

    return return_data
