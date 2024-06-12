from . import imageProcessing as ip
from .models import Attribute, Operation, Parameter

def Apply(image, selected_process, request, history_entry):

    # Fetch the operation object
    operation = Operation.objects.get(name=selected_process)

    # Fetch all parameters associated with this operation
    parameters = Parameter.objects.filter(oprID=operation)

    # Create a dictionary to store parameter values
    param_values = {}

    for param in parameters:
        param_value = request.GET.get(param.name)
        if param_value == "" or param_value is None:
            param_value = param.default_value  # Assuming there's a default value in the model, or handle it as needed
        if param.valueType == 'number':
            param_value = int(param_value)
        elif param.valueType == 'float':
            param_value = float(param_value)
        
        param_values[param.name] = param_value
        Attribute.objects.create(name=param.name, value=str(param_value), history=history_entry)

    # Call the corresponding image processing function
    if selected_process == 'Blur':
        return ip.blur(image, param_values.get('Kernel Size'))
    elif selected_process == 'Sharpen':
        return ip.sharpen(image, param_values.get('Kernel Size'))
    elif selected_process == 'Median':
        return ip.median(image, param_values.get('Kernel Size'))
    elif selected_process == 'Grayscale':
        return ip.grayscale(image)
    elif selected_process == 'Invert':
        return ip.invert(image)
    elif selected_process == 'Threshold':
        return ip.threshold(image, param_values.get('Threshold'))
    elif selected_process == 'Gaussian Blur':
        return ip.gaussian_blur(image, param_values.get('Kernel Size'), param_values.get('Standard Deviation', 1.0))
    elif selected_process == 'RGB separation':
        return ip.rgb_separation(image, channel= "green")
    elif selected_process == 'Brighten':
        return ip.brighten(image, constant= param_values.get('Constant'))
    elif selected_process == 'Darken':
        return ip.darken(image, constant= param_values.get('Constant'))
    elif selected_process == 'Bilateral':
        return ip.bilateral(image, param_values.get('Kernel Size'))

    # Add more operations as needed
