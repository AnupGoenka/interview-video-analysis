import base64
import os
import random
from json import dumps
from time import sleep, time

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from redis import Redis
from rq import Queue
from rq.job import Job

from vision import BASE_DIR, app  # , job_queue
from vision.api.microexpression_analysis import VIA


def sett(s):
    sleep(2)
    return "Hi"

@app.route('/heatlh_check')
def healthCheck():
    return("vision_analyser",200)

@app.route('/')
def index():
    return ('Working', 200)

@app.route('/vision_analysis',methods=['POST'])
def vision():
    # global worker_dic
    response = {
        'status_code': 500,
        'message': 'Failed to queue vision analysis job'
    }
    try:

        # videoData   = request.stream.read()
        userId      = request.args.get('user_id')
        redisKey    = request.args.get('redis_key')
        count       = request.args.get('count')
        print('User ID :', userId)
        print('Redis key : ', redisKey)
        print('Count: ', count)
        filepath = request.args.get('filepath')
        print('filepath :', filepath)
        filename = request.args.get('filename')
        print('filename: ', filename)
        videoName = filename
        videoPath = filepath
        currentTime = str(int(time()))
        videoName = userId + currentTime + str(random.randint(1,999999)) + '.png'
        videoPath = BASE_DIR + '/video_files/'
        # prin/t('Video name and video path : ',videoName, videoPath)
        start = time()
        with open(videoPath + videoName, "wb") as vid:
            video_stream = base64.b64decode(videoData.decode().partition(",")[2])
            # print(type(video_stream))
            vid.write(video_stream)

        result = q_visual.enqueue_call(VIA, args=(videoName, videoPath), timeout=15)
        # VIA(videoName, videoPath)


        VIA(filename, filepath,redisKey)
        # print(filepath+filename)

        VIA(videoName, videoPath,redisKey, userId, count) 
        end = time()
        print('code completion time:', end-start)
        
        response['message'] = "Successfully queued vision analysis job."
        response['status_code'] = "200"
    except Exception as e:
        raise Exception(e)
    return dumps(response)