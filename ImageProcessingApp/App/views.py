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
import zipfile
import shutil

UPLOAD_FOLDER = 'uploads'
BATCH_FOLDER = 'batchUploads'
EXTRACTED_BATCH_FOLDER = os.path.join(BATCH_FOLDER, 'extracted')
PROCESSED_BATCH_FOLDER = 'processedBatchUploads'
COMPRESSED_BATCH_FOLDER = 'compressedBatch'
image_path = os.path.join(UPLOAD_FOLDER, "image")
processed_image_path = os.path.join(UPLOAD_FOLDER, "processed_image.png")
batch_path = os.path.join(BATCH_FOLDER, "zipFile.zip")
compressed_batch_path = os.path.join(COMPRESSED_BATCH_FOLDER, 'processedZipFile.zip')


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
    
def uploadZip(request):

    if not os.path.exists(BATCH_FOLDER):
        os.makedirs(BATCH_FOLDER)
    

    if not os.path.exists(PROCESSED_BATCH_FOLDER):
        os.makedirs(PROCESSED_BATCH_FOLDER)
    else:
        try:
            shutil.rmtree(PROCESSED_BATCH_FOLDER)
            print(f"Deleted folder: {PROCESSED_BATCH_FOLDER}")
            os.makedirs(PROCESSED_BATCH_FOLDER)
        except Exception as e:
            print(f"Failed to delete folder: {PROCESSED_BATCH_FOLDER} - {e}")
        


    if not os.path.exists(EXTRACTED_BATCH_FOLDER):
        os.makedirs(EXTRACTED_BATCH_FOLDER)
    else:
        try:
            shutil.rmtree(EXTRACTED_BATCH_FOLDER)
            print(f"Deleted folder: {EXTRACTED_BATCH_FOLDER}")
            os.makedirs(EXTRACTED_BATCH_FOLDER)
        except Exception as e:
            print(f"Failed to delete folder: {EXTRACTED_BATCH_FOLDER} - {e}")
        

    if not os.path.exists(COMPRESSED_BATCH_FOLDER):
        os.makedirs(COMPRESSED_BATCH_FOLDER)
    else:
        try:
            shutil.rmtree(COMPRESSED_BATCH_FOLDER)
            print(f"Deleted folder: {COMPRESSED_BATCH_FOLDER}")
            os.makedirs(COMPRESSED_BATCH_FOLDER)
        except Exception as e:
            print(f"Failed to delete folder: {COMPRESSED_BATCH_FOLDER} - {e}")

    if request.method == 'POST':

        if 'sourceDirectory' in request.FILES:
            zipFile = request.FILES['sourceDirectory']

            # Save uploaded zip file
            with open(batch_path, 'wb+') as destination:
                for chunk in zipFile.chunks():
                    destination.write(chunk)

            # Extract zip file
            with zipfile.ZipFile(batch_path, 'r') as zip_ref:
                zip_ref.extractall(EXTRACTED_BATCH_FOLDER)

            file_paths = [os.path.join(root, file) for root, _, files in os.walk(EXTRACTED_BATCH_FOLDER) for file in files]

            for file_path in file_paths:
                relative_path = os.path.relpath(file_path, EXTRACTED_BATCH_FOLDER)
                new_path = os.path.join(PROCESSED_BATCH_FOLDER, relative_path)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.jfif')):
                    try:
                        img = cv2.imread(file_path)
                        if img is not None:
                            # Perform your image processing here
                            print(f"Processing image: {file_path}")

                            processed_image = img

                            for entry in History.objects.all():
                                processed_image = ApplyUpdates(processed_image, entry)

                            # Save the processed image to new_path
                            try:
                                cv2.imwrite(new_path, processed_image)
                            except:
                                cv2.imwrite(new_path+'.png', processed_image)
                        else:
                            print(f"Failed to read image: {file_path}")
                    except Exception as e:
                        print(f"Error processing image {file_path}: {e}")
                else:
                    shutil.copy(file_path, new_path)
            
            # Compress the processed files into a new zip file
            with zipfile.ZipFile(compressed_batch_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(PROCESSED_BATCH_FOLDER):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, PROCESSED_BATCH_FOLDER)
                        print(f"Compressing image: {file_path}")
                        zipf.write(file_path, arcname)
            
            return HttpResponse("Successfully processed")
      
    return HttpResponse("Failed")


def downloadBatchAsZip(request):
    if os.path.exists(compressed_batch_path):
        return FileResponse(open(compressed_batch_path, 'rb'), as_attachment=True, filename='processed_dataSet.zip')
    return HttpResponse('Failed')