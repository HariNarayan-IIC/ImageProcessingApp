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

#Filters
def sharpen(image):
    kernel = np.ones(shape=(3,3)) * -1
    kernel[1,1] = 9
    return cv.filter2D(image, -1, kernel)

def blur(image):
    kernel = np.ones(shape= (3,3)) * (1/9)
    return cv.filter2D(image, -1, kernel)

def median(image, k= 3):
    return cv.medianBlur(image, k)