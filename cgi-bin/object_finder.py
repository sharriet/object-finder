#!/usr/bin/env python3

""" Simple object detection from images using OpenCV
    Use this script to locate objects in an image or webcam feed and
    output their locations along with the image dimensions.
    Not rigourously tested!

    See README for useage examples.
    
    Resources used to create this script:
    - Getting started with images in opencv:
        https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_image_display/py_image_display.html
    - Image thresholding tutorial:
        https://www.pyimagesearch.com/2017/08/28/fast-optimized-for-pixel-loops-with-opencv-and-python/
"""
import sys
import json
import numpy as np
import cv2
from matplotlib import pyplot as plt
from random import randint
from statistics import mean

def capture(src=0):
    """ Capture continuously from a specified input source

        :param src: the input source as int
    """
    # create capture object from specified source
    cap = cv2.VideoCapture(src)

    # check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video stream or file")

    # read frames
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Frame', frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()

def capture_once(src=0):
    """ Capture a single image from webcam

        :param src: the input source as int
        :returns: pixel data
    """
    # uses input 1 on my laptop
    cap = cv2.VideoCapture(src)
    ret, frame = cap.read() # Read the frame
    cap.release()
    return frame

def find_objs(T_bw, T_p, image):
    """ Identifies objects in an image by converting to black and white
        and grouping the black pixels according to a proximity 
        threshold.

        Use a larger proximity threshold for widely spaced objects to
        speed up computation.

        :param T_bw: black and white threshold (0-255)
        :param T_p: pixel proximity threshold (0-image width)
        :returns: list of coordinates in following format: 
                    [[y0,x0], [y1,x1]...[yn,xn]]
    """
    def threshold_bw(T_bw, image):
        # loop over the image, pixel by pixel
        for y in range(0, h):
            for x in range(0, w):
                # threshold the pixel
                image[y, x] = 255 if image[y, x] >= T_bw else 0
        # return the thresholded image
        return image

    def find_close_pixels(group, data):
        for yc, xc in group:
            for y, x in data:
                if abs(yc-y)<=T_p and abs(xc-x)<=T_p:
                    group.append((y,x))
                    data.remove((y,x))
        return group, data

    def group_pixels(data):
        groups = []
        while len(data) > 0:
            pix = data[0]
            data.remove(pix)
            group, data = find_close_pixels( [pix], data )
            groups.append(group)
        return groups

    # convert image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # grab the image dimensions
    h = image.shape[0]
    w = image.shape[1]

    # convert image to black and white
    image = threshold_bw(T_bw, image)

    # get the black pixel locs in a list
    black_pixels = []

    # loop over the image, pixel by pixel
    for y in range(0, h):
        for x in range(0, w):
            if image[y,x] == 0:
                black_pixels.append( (y, x) )

    # check ratio of black to white pixels
    if len(black_pixels)/(h*w) > 0.1:
        return

    # group the black pixel data 
    groups = group_pixels(black_pixels)

    # get centres of the groups from average y and x
    f = lambda g: [ int(mean(t)) for t in list(zip(*g)) ]
    obj_locs = [ f(group) for group in groups ]

    return obj_locs

def visualise_objects(image, arr):
    """
        Overlay current image with red squares to indicate suspected
        object locations. Useful for testing purposes.

        :param image: the image upon which to plot object locations
        :param arr: an array of coordinates in following format:
                    [[y0,x0],[y1,x1]...[yn,xn]]
        :returns: the modified image
    """
    for y,x in arr:
        image[y:y+5,x:x+5] = [255,0,0]
    # plot it
    plt.imshow(image)
    plt.show()
    return

def test_camera(src=0):
    """ Capture continuously.
        Test your webcam is lined up!
        Quit with 'q' """
    capture(src=src)
    plt.show()

def trigger_capture(url=None, src=0, T_bw=50, T_p=50):
    """ Trigger an image capture from an image URL or from a camera
        source and locate the objects in it.

        :param url: image URL
        :param src: the input source
        :param T_bw: the threshold for B+W image conversion (0-255)
        :param T_p: the pixel proximity threshold for object detection

        :returns: the image and an array of object locations
    """
    # read in an image from file
    if url is not None:
        try:
            img = cv2.imread(url)
        except IOError:
            err = "The image could not be loaded from supplied URL."
            print(json.dumps({"error": err}))
    # capture one image (for analysis)
    else:
        try:
            img = capture_once(src=src)
        except:
            err = "Problem capturing image. Check the source."
            print(json.dumps({"error": err}))

    try: img
    except NameError:
        err = "Problem capturing image. Check the source."
        print(json.dumps({"error": err}))
    else:
        # try to locate the objects in the image
        obj_arr = find_objs(T_bw, T_p, img)
    
    try: obj_arr
    except NameError:
        err = "No objects detected. Try adjusting b+w and/or proximity thresholds."
    else:
        # output the object location data in JSON format
        data = json.dumps({"w": img.shape[1], "h": img.shape[0], "locs": obj_arr})    
        print(data)

        return img, obj_arr
