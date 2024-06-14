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
    return cv.Laplacian(image, -1)

#Histogram
def histogram_equalization(image):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return cv.equalizeHist(gray_image)

def clahe(image, clipLimit= 2, k= 8):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    clahe = cv.createCLAHE(clipLimit=clipLimit, tileGridSize=(k,k))
    return clahe.apply(gray_image)


#Morphological
def erosion(image, k=3, i=1):
    kernel= np.ones((k,k), np.uint8)
    return cv.erode(image, kernel, iterations= i)

def dialtion(image, k= 3, i=1):
    kernel= np.ones((k,k), np.uint8)
    return cv.dilate(image, kernel, iterations= i)

def opening(image, k= 3):
    kernel= np.ones((k,k), np.uint8)
    return cv.morphologyEx(image, cv.MORPH_OPEN, kernel)

def closing(image, k= 3):
    kernel= np.ones((k,k), np.uint8)
    return cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)

#Image segmentation
def adaptive_thresholding(image, type, k):
    print(k)
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    if type == "Mean":
        return cv.adaptiveThreshold(gray_image,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,k,2)
    else:
        return cv.adaptiveThreshold(gray_image,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,k,2)

def k_means_clustering(image, K= 8):
    Z = image.reshape((-1,3))
 
    # convert to np.float32
    Z = np.float32(Z)
    
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    ret,label,center=cv.kmeans(Z,K,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
    
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))
    return res2

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