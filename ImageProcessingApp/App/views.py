from django.shortcuts import render, HttpResponse
from django.http import FileResponse, Http404
from django.http import JsonResponse
from .apply import Apply
from .applyUpdates import ApplyUpdates
from .models import *
from django.db.models import Q
import cv2
import os
import base64

UPLOAD_FOLDER = 'uploads'
image_path = os.path.join(UPLOAD_FOLDER, "image")
processed_image_path = os.path.join(UPLOAD_FOLDER, "processed_image.png")

# Create your views here.
def mainView(request):
    return render(request, "index.html")

def upload(request):
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if request.method == 'POST':
        # Check if the form is valid
        if 'image' in request.FILES:
            History.objects.all().delete()
            image = request.FILES['image']

            # Save the uploaded image
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
            attribute_entries = Attribute.objects.all()
            category_entries = Category.objects.all()
            data = {
                "original_image_base64":original_image_base64,
                "history_entries":history_entries,
                "attribute_entries": attribute_entries,
                "category_entries": category_entries,
            }

            return render(request, 'editor.html', data)
        
        else:
                return render(request, 'index.html',{"Message": 'No image uploaded.'})
    else:
        # Render the form if the request is not a POST request
        return render(request, 'index.html')

def load_operations(request):
    category_id = request.GET.get('category_id')
    operations = Operation.objects.filter(catID=category_id).all()
    return JsonResponse(list(operations.values('id', 'name')), safe=False)

def load_parameters(request):
    if (request.GET.get('type')=="apply"):
        operation_id = request.GET.get('operation_id')
    elif (request.GET.get('type')=="update"):
        history_id = request.GET.get('history_id')
        operation_id = Operation.objects.get(name= History.objects.get(id=history_id).operation).id

    parameters = Parameter.objects.filter(oprID=operation_id).all()
    return JsonResponse(list(parameters.values('id', 'name', 'inputType', 'minValue', 'maxValue')), safe=False)

def load_options(request):
    parameter_id = request.GET.get('parameter_id')
    options = Option.objects.filter(parameter=parameter_id).all()
    return JsonResponse(list(options.values('id', 'optionNo', 'value')), safe=False)

def apply(request):

    original_image_path= os.path.join(UPLOAD_FOLDER, "image")
    processed_image_path = os.path.join(UPLOAD_FOLDER, "processed_image.png")

    #Check if processed image already exists
    image = cv2.imread(processed_image_path)
    if image is None:
        image= cv2.imread(original_image_path)
    selected_id = request.GET.get('selected_process', 'Grayscale')
    selected_process = Operation.objects.get(id= selected_id).name

    # Save selected_process to History table
    history_entry = History.objects.create(operation=selected_process)

    #Apply image processing
    processed_image= Apply(image, selected_process, request, history_entry)

    #Save processed image
    cv2.imwrite(processed_image_path, processed_image) 

    #Encode processed image as base64
    retval, buffer = cv2.imencode('.jpg', processed_image)
    original_image_base64 = base64.b64encode(buffer).decode('utf-8')
    history_entries = History.objects.all()
    attribute_entries = Attribute.objects.all()
    category_entries = Category.objects.all()
    data = {
        "original_image_base64":original_image_base64,
        "history_entries":history_entries,
        "attribute_entries": attribute_entries,
        "category_entries": category_entries,
    }
    
    return render(request, 'editor.html', data)

def delete(request, history_id):
    try:
        # Find the history entry with the given id
        history_entry = History.objects.get(id=history_id)
        # Delete the history entry
        history_entry.delete()
    except History.DoesNotExist:
        pass

    #Reset Processed image
    uploaded_image = cv2.imread(image_path)
    cv2.imwrite(processed_image_path, uploaded_image)
    processed_image = cv2.imread(processed_image_path)

    for entry in History.objects.all():
        processed_image = ApplyUpdates(processed_image, entry)
        cv2.imwrite(processed_image_path, processed_image)

    # Encode the original image as base64
    retval, buffer = cv2.imencode('.jpg', processed_image)
    original_image_base64 = base64.b64encode(buffer).decode('utf-8')
    history_entries = History.objects.all()
    attribute_entries = Attribute.objects.all()
    category_entries = Category.objects.all()
    data = {
        "original_image_base64":original_image_base64,
        "history_entries":history_entries,
        "attribute_entries": attribute_entries,
        "category_entries": category_entries,
    }
    return render(request, "editor.html", data)

def update(request):
    try:
        # Find the history entry with the given id
        history_entry = History.objects.get(id=request.GET.get('history_id'))

        # Update the history entry
        operation = Operation.objects.get(name=history_entry.operation)

        # Fetch all parameters associated with this operation
        parameters = Parameter.objects.filter(oprID=operation)

        # Create a dictionary to store parameter values
        param_values = {}

        for param in parameters:
            param_value = request.GET.get(param.name)  
            if param_value == "" or param_value is None:
                param_value = param.defaultValue  # Assuming there's a default value in the model, or handle it as needed
            if param.dataType == 'int':
                param_value = int(param_value)
            elif param.dataType == 'float':
                param_value = float(param_value)
            elif param.dataType == 'str':
                param_value = str(param_value)
            
            param_values[param.name] = param_value
            att_entity= Attribute.objects.get(name=param.name, history=history_entry.id)

            att_entity.value= param_values.get(param.name)
            att_entity.save()
    except History.DoesNotExist:
        pass

    #Reset Processed image
    uploaded_image = cv2.imread(image_path)
    cv2.imwrite(processed_image_path, uploaded_image)
    processed_image = cv2.imread(processed_image_path)


    for entry in History.objects.all():
        processed_image = ApplyUpdates(processed_image, entry)
        cv2.imwrite(processed_image_path, processed_image)
    print("\n\nI am here \n\n")
    # Encode the original image as base64
    retval, buffer = cv2.imencode('.jpg', processed_image)
    original_image_base64 = base64.b64encode(buffer).decode('utf-8')
    history_entries = History.objects.all()
    attribute_entries = Attribute.objects.all()
    category_entries = Category.objects.all()
    data = {
        "original_image_base64":original_image_base64,
        "history_entries":history_entries,
        "attribute_entries": attribute_entries,
        "category_entries": category_entries,
    }
    return render(request, "editor.html", data)

def reset(request):
    #Reset History table from database
    History.objects.all().delete()

    #Change the image back to original image
    uploaded_image = cv2.imread(image_path)
    cv2.imwrite(processed_image_path, uploaded_image)

    # Encode the original image as base64
    retval, buffer = cv2.imencode('.jpg', uploaded_image)
    original_image_base64 = base64.b64encode(buffer).decode('utf-8')
    history_entries = History.objects.all()
    attribute_entries = Attribute.objects.all()
    category_entries = Category.objects.all()
    data = {
        "original_image_base64":original_image_base64,
        "history_entries":history_entries,
        "attribute_entries": attribute_entries,
        "category_entries": category_entries,
    }
    return render(request, "editor.html", data)

def download(request):
    file_path = os.path.join(UPLOAD_FOLDER, "processed_image.png")
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='processed_image.png')
    else:
        raise Http404("File does not exist")
    
def fetch_parameters(request):
    history_id = request.GET.get('historyId')
    parameters = Parameter.objects.filter(history_id=history_id)
    parameter_list = [{'name': param.name, 'value': param.value} for param in parameters]
    return JsonResponse({'parameters': parameter_list})

def fetch_options(request):
    return

def update_parameters(request):
    if request.method == 'POST':
        history_id = request.POST.get('historyId')
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'historyId':
                parameter = Parameter.objects.get(name=key, history_id=history_id)
                parameter.value = value
                parameter.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})