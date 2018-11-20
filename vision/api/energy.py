## Capturing micro expression movement
## more movement more energy and visa versa
from vision import BASE_DIR
from vision.api.MicroExpresssion import ALLemotions
import multiprocessing
import random

def energy(key_cord, pupil_data, emotion, shape):
    # print('********** In energy ***************')
    # emotions_queue = multiprocessing.Queue()
    micro_expression_data = ALLemotions(shape, key_cord)
    
    # micro_expression_p.start()
    
    # micro_expression_data = emotions_queue.get()
    
    # micro_expression_p.join()
    
    energy = micro_expression_data['eyebrow']*0.5+micro_expression_data['lips']*0.5
    # energy = energy/4
    # print('********At the end of energy data***********', energy)
    return(energy if energy<94 else random.randint(85,100))
    

    