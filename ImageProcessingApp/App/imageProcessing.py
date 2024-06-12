import cv2 as cv
import numpy as np


#Pixel processing
def grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def invert(image):
    return 255-image

def threshold(image, t= 126):
    t, output= cv.threshold(image, t, 255, cv.THRESH_BINARY)
    return output

def rgb_separation(image, channel= "green"):
    b,g,r = cv.split(image)
    if channel == "red":
        return r
    elif channel == "green":
        return g
    else:
        return b

def brighten(image, constant):
    return cv.convertScaleAbs(image, alpha= 1, beta= constant)

def darken(image, constant):
    return cv.convertScaleAbs(image, alpha= 1, beta= -constant)

#Filters
def sharpen(image, k= 3):
    kernel = np.ones(shape=(k,k)) * -1
    kernel[1,1] = 9
    return cv.filter2D(image, -1, kernel)

def blur(image, k= 3):
    kernel = np.ones(shape= (k,k)) * (1/9)
    return cv.filter2D(image, -1, kernel)

def median(image, k= 3):
    return cv.medianBlur(image, k)

def gaussian_blur(image, k= 3, std_dev= 1):
    return cv.GaussianBlur(image, (k, k), std_dev)

def bilateral(image, k= 3):
    return 