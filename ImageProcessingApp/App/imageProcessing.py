import cv2
import numpy as np

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def sharpen(image):
    kernel = np.ones(shape=(3,3)) * -1
    kernel[1,1] = 9
    return cv2.filter2D(image, -1, kernel)

def blur(image):
    kernel = np.ones(shape= (3,3)) * (1/9)
    return cv2.filter2D(image, -1, kernel)