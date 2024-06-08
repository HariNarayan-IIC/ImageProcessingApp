from . import imageProcessing as ip
from .models import Attribute, Operation, Parameter

def ApplyUpdates(image, entry):
    selected_process = entry.operation
    history_id = entry.id

    # Fetch the operation object
    operation = Operation.objects.get(name=selected_process)

    # Fetch all parameters associated with this operation
    parameters = Parameter.objects.filter(oprID=operation)

    # Create a dictionary to store parameter values
    param_values = {}

    for param in parameters:
        attribute = Attribute.objects.get(history=history_id, name=param.name)
        param_value = attribute.value

        # Convert the parameter value to the correct type
        if param.valueType == 'number':
            param_value = int(param_value)
        elif param.valueType == 'float':
            param_value = float(param_value)

        param_values[param.name] = param_value

    # Call the corresponding image processing function
    if selected_process == 'Blur':
        return ip.blur(image)
    elif selected_process == 'Sharpen':
        return ip.sharpen(image)
    elif selected_process == 'Median':
        return ip.median(image)
    elif selected_process == 'Grayscale':
        return ip.grayscale(image)
    elif selected_process == 'Invert':
        return ip.invert(image)
    elif selected_process == 'Threshold':
        return ip.threshold(image, param_values.get('Threshold', 126))
    elif selected_process == 'Gaussian Blur':
        return ip.gaussian_blur(image, param_values.get('Kernel Size', 3), param_values.get('Standard Deviation', 1.0))

    # Add more operations as needed
