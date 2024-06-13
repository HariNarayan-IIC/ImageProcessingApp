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

def rgb_separation(image, channel= "Green"):
    b,g,r = cv.split(image)
    if channel == "Red":
        return r
    elif channel == "Green":
        return g
    else:
        return b

def brighten(image, constant):
    print(type(constant))
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

def bilateral(image, k= 3, sigmaColor= 1, sigmaSpace= 1):
    return cv.bilateralFilter(image, -1, sigmaColor, sigmaSpace)

#Edge Detection
def sobel(image, t):
    kernel = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
    sobel1= cv.filter2D(image, -1, kernel)
    sobel2= cv.filter2D(image, -1, kernel)
    Sobel= sobel1 + sobel2
    ret, thrSobel= cv.threshold(Sobel, t, 255, cv.THRESH_BINARY)
    return thrSobel

def canny(image, t_1, t_2):
    return cv.Canny(image, t_1, t_2)

def laplacian(image):
    return

#Histogram
def histogram_equalization(image):
    return

def clahe(image):
    return

#Morphological
def erosion(image):
    return

def dialtion(image):
    return

def opening(image):
    return

def closing(image):
    return

#Image segmentation
def adaptive_thresholding(image):
    return

def k_means_clustering(image):
    return

#Geometrical
def resize(image):
    return 

def rotate_right_by_90(image):
    return cv.rotate(image, cv.ROTATE_90_CLOCKWISE)

def rotate_left_by_90(image):
    return cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)

def rotate_180(image):
    return cv.rotate(image, cv.ROTATE_180)

def horizontal_flip(image):
    return cv.flip(image, 1)

def vertical_flip(image):
    return cv.flip(image, 0)