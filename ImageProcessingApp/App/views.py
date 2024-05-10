from django.shortcuts import render, HttpResponse
from . import imageProcessing as ip
import cv2
import os
import base64

UPLOAD_FOLDER = 'uploads'

# Create your views here.
def mainView(request):
    return render(request, "index.html")

def upload(request):
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if request.method == 'POST':
        # Check if the form is valid
        if 'image' in request.FILES:
            image = request.FILES['image']

            # Save the uploaded image to disk
            image_path = os.path.join(UPLOAD_FOLDER, "image")
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Read the saved image using OpenCV
            uploaded_image = cv2.imread(image_path)

            # Encode the original image as base64
            retval, buffer = cv2.imencode('.jpg', uploaded_image)
            original_image_base64 = base64.b64encode(buffer).decode('utf-8')

            data = {
                "original_image_base64":original_image_base64,
            }

            return render(request, 'editor.html', data)
        
        else:
                return render(request, 'index.html',{"Message": 'No image uploaded.'})
    else:
        # Render the form if the request is not a POST request
        return render(request, 'index.html')

def apply(request):
    image_path = os.path.join(UPLOAD_FOLDER, "image")
    original_image = cv2.imread(image_path)
    processed_image= ip.grayscale(original_image)
    retval, buffer = cv2.imencode('.jpg', processed_image)
    original_image_base64 = base64.b64encode(buffer).decode('utf-8')
    data = {
                "original_image_base64":original_image_base64,
    }
    return render(request, 'editor.html', data)