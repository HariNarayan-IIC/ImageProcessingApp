from django.shortcuts import render, HttpResponse
from . import imageProcessing as ip
import cv2
import os
import base64


# Create your views here.
def mainView(request):
    return render(request, "index.html")

def upload(request):
    UPLOAD_FOLDER = 'uploads'
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

            processing_method = request.POST.get('processing_method', 'grayscale')

            # Apply selected image processing method
            if processing_method == 'grayscale':
                processed_image = ip.grayscale(uploaded_image)

            elif processing_method == 'sharpen':
                processed_image = ip.sharpen(uploaded_image)

            elif processing_method == 'blur':
                processed_image = ip.blur(uploaded_image)

            # Encode the processed image as base64
            retval, buffer = cv2.imencode('.jpg', processed_image)
            processed_image_base64 = base64.b64encode(buffer).decode('utf-8')

            # Encode the original image as base64
            retval, buffer = cv2.imencode('.jpg', uploaded_image)
            original_image_base64 = base64.b64encode(buffer).decode('utf-8')

            # Cleanup: Remove the uploaded image file from disk
            os.remove(image_path)
            data = {
                "original_image_base64":original_image_base64,
                "processed_image_base64":processed_image_base64
            }

            return render(request, 'index.html', data)
        
        else:
                return HttpResponse('No image uploaded.', status=400)
    else:
        # Render the form if the request is not a POST request
        return render(request, 'upload_image.html')

