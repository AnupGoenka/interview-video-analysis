import argparse
import logging
import sys
import time
from vision import BASE_DIR
from  vision.api.tf_pose import common
import cv2
import numpy as np
from  vision.api.tf_pose.estimator import TfPoseEstimator
from  vision.api.tf_pose.networks import get_graph_path, model_wh
import multiprocessing


logger = logging.getLogger('TfPoseEstimator')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def main_fun( image, queue1, lock):
    resize = '432x368'
    model = 'mobilenet_thin'
    resize_out_ratio = 4.0
    w, h = model_wh(resize)
    if w == 0 or h == 0:
        e = TfPoseEstimator(get_graph_path(model), target_size=(432, 368))
    else:
        e = TfPoseEstimator(get_graph_path(model), target_size=(w, h))
        
                                                                                               
    image = common.read_imgfile(image, None, None)
    try:
        if image is None:
            logger.error('Image can not be read, path=%s' % image)
            sys.exit(-1)
    except Exception as e:
        print('This exception:',e)
    try:
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
    except Exception as e:
        print('That exception: ',e)
    
    key_cord = {}
    try:
        values = humans[0].body_parts.values()
        keys = humans[0].body_parts.keys()
    except:
        pass

    i = 0
    try:
        for key in list(keys):
            if(key<9):
                key_cord[key] = {
                            'x' : float(str(list(values)[i]).split('(')[1].split(')')[0].split(',')[0]),
                            'y' : float(str(list(values)[i]).split('(')[1].split(')')[0].split(',')[1])
                        }
            else:
                key_cord[key] = {
                            'x' : float(str(list(values)[i]).split('(')[1].split(')')[0].split(',')[0]),
                            'y' : float(str(list(values)[i]).split('(')[1].split(')')[0].split(',')[1])
                        }
            i = i + 1
    except Exception as e:
        key_cord = None
    lock.acquire()
    queue1.put(key_cord)
    lock.release()
