# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 19:54:05 2022

@author: André
"""

import os
import tensorflow as tf
import ffmpeg
import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt
import argparse
#import matplotlib as matt
#print(matt.get_backend())

#link = r"D:\School\masterthesis\Recordings"#r"\Recordings\843808.mp4"



def process_img(img):
  
  startY = len(img[0]) * 0.1  #  10% from top
  endY = len(img[0]) * 0.75   # keep 75# to the right
  startX = len(img[:,0]) * 0.1 # remove 10 % from left
  endX = len(img[:,0])
  img = img[int(startX):int(endX), int(startY):int(endY)]

  img = tf.image.per_image_standardization(img) # standartize with mean = 0 and std=1
  img = tf.image.resize(img, (224, 224)) # reshape for densenet
  img = np.expand_dims(img, axis=0)   # expand (224, 224, 3) -> (1, 224, 224, 3)

  return img

def binary_search(start_range, index):


  if len(start_range) < 2:
    return
  
  current_range = start_range
  middle_frame = len(current_range)/2
  middle_frame = int(middle_frame)
  print(middle_frame, middle_frame+index)
  
  vidcap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame+index)
  success, frame = vidcap.read()

  if not success:
    print("ERROR reading in image")
    return


  img = process_img(frame)

  pred = ZFnetmodel.predict(img)
  # append predicted labels
  print("Percentage: ", pred)
  if pred > 0.5:
    print("This image shows fault")
    frames_of_faults.append(middle_frame+index)
    binary_search(current_range[:middle_frame], index)
  else:
    print("No fault in image")
    binary_search(current_range[middle_frame:], middle_frame+index)
  
  #y_pred.append((1 if preds > 0.5 else 0))

def pred_all():
    framenr = 0
    success, frame = vidcap.read()
    while success:
    
        success, frame = vidcap.read()

        if framenr % 3 == 0:
            img = process_img(frame)
            pred = ZFnetmodel.predict(img)
            print("Framenr: ", framenr)
            print("Percentage: ", pred)

            if pred > 0.5:
                print("This image shows fault")
                return framenr
            else:
                print("No fault in image")
        
        framenr += 1
    return 0


if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Filename")
    parser.add_argument("-s", "--fromstart", action='store_true', help="Run from start")
    args = parser.parse_args()


    link = args.filename  #"./843808.mp4"


    vid = ffmpeg.probe(link)
    vidcap = cv2.VideoCapture(link)

    #success. frame = vidcap.read()
    #vidcap.set(cv2.CAP_PROP_POS_FRAMES, 1900)

    dur = vid['streams'][0]['duration']
    framestot = vid['streams'][0]['nb_frames']
    fps = vid['streams'][0]['r_frame_rate']

    #print(dur)
    #print(framestot)
    #print(fps)

    avgfps = int(float(framestot)/float(dur))

    #print(avgfps)
    #tf.config.list_physical_devices('GPU')
    try:
        ZFnetmodel = tf.keras.models.load_model('./my_model')
        # Check its architecture
        #new_model.summary()
        print("ZFnetmodel loaded.")
    except:
        sys.exit("ERROR: Couldn't load model.")

    #frametocheck = int(float(framestot)/float(2))
    frametocheck = 0

    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frametocheck)
    success, frame = vidcap.read()
    
    if not success:
        print("ERROR reading in image")
        sys.exit()



    # PREPROCESS CUTTING AS TRAINING DID

    ####

    start_range = range(int(framestot))
    frames_of_faults = []

    if args.fromstart:
        framenr = pred_all()
        if framenr >= 1:
            print(framenr)
            print("Earliest fault found at: ", framenr/avgfps, " seconds")
        else:
            print("No faults found")
    else:
        binary_search(start_range, 0)
        if len(frames_of_faults) >= 1:
            print(frames_of_faults)
            print("Earliest fault found at: ", frames_of_faults[-1]/avgfps, " seconds")
        else:
            print("No faults found")






