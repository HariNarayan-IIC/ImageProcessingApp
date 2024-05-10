from django.shortcuts import render, HttpResponse
from .apply import Apply
from .models import History
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
            processed_image_path = os.path.join(UPLOAD_FOLDER, "processed_image.png")

            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Read the saved image using OpenCV
            uploaded_image = cv2.imread(image_path)
            cv2.imwrite(processed_image_path, uploaded_image) 

            # Encode the original image as base64
            retval, buffer = cv2.imencode('.jpg', uploaded_image)
            original_image_base64 = base64.b64encode(buffer).decode('utf-8')
            history_entries = History.objects.all()
            data = {
                "original_image_base64":original_image_base64,
                "history_entries":history_entries,
            }

            return render(request, 'editor.html', data)
        
        else:
                return render(request, 'index.html',{"Message": 'No image uploaded.'})
    else:
        # Render the form if the request is not a POST request
        return render(request, 'index.html')

def apply(request):
    original_image_path= os.path.join(UPLOAD_FOLDER, "image")
    processed_image_path = os.path.join(UPLOAD_FOLDER, "processed_image.png")

    #Check if processed image already exists
    image = cv2.imread(processed_image_path)
    if image is None:
        image= cv2.imread(original_image_path)
    selected_process = request.GET.get('selected_process', 'grayscale')

    # Save selected_process to History table
    history_entry = History.objects.create(operation=selected_process)

    #Apply image processing
    processed_image= Apply(image, selected_process)

    #Save processed image
    cv2.imwrite(processed_image_path, processed_image) 

    #Encode processed image as base64
    retval, buffer = cv2.imencode('.jpg', processed_image)
    original_image_base64 = base64.b64encode(buffer).decode('utf-8')
    history_entries = History.objects.all()
    data = {
        "original_image_base64":original_image_base64,
        "history_entries":history_entries,
    }
    
    return render(request, 'editor.html', data)