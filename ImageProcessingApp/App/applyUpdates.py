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
        if param.dataType == 'number':
            param_value = int(param_value)
        elif param.dataType == 'float':
            param_value = float(param_value)
        elif param.dataType == 'string':
            continue

        param_values[param.name] = param_value

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
        return ip.rgb_separation(image, channel= param_values.get('Channel'))
    elif selected_process == 'Brighten':
        return ip.brighten(image, constant= param_values.get('Brighten by'))
    elif selected_process == 'Darken':
        return ip.darken(image, constant= param_values.get('Darken by'))
    elif selected_process == 'Bilateral':
        return ip.bilateral(image, param_values.get('Kernel Size'), param_values.get('Std Dev Color'), param_values.get('Std Dev Space'))
    elif selected_process == 'Rotate 90 Clockwise':
        return ip.rotate_right_by_90(image)
    elif selected_process == 'Rotate 90 Anticlockwise':
        return ip.rotate_left_by_90(image)
    elif selected_process == 'Rotate 180':
        return ip.rotate_180(image)
    elif selected_process == 'Horizontal Flip':
        return ip.horizontal_flip(image)
    elif selected_process == 'Vertical Flip':
        return ip.vertical_flip(image)
    elif selected_process == 'Sobel':
        return ip.sobel(image, param_values.get('Threshold'))
    elif selected_process == "Canny":
        return ip.canny(image, param_values.get('Threshold 1'), param_values.get('Threshold 2'))
    elif selected_process == "Laplacian":
        return ip.laplacian(image)
    elif selected_process == "Global HE":
        return ip.histogram_equalization(image)
    elif selected_process == "CLAHE":
        return ip.clahe(image, param_values.get('Clip Limit'), param_values.get('Tile Size'))
    elif selected_process == 'Erosion':
        return ip.erosion(image, param_values.get('Kernel Size'), param_values.get('Iterations'))
    elif selected_process == 'Dilation':
        return ip.dialtion(image, param_values.get('Kernel Size'), param_values.get('Iterations'))
    elif selected_process == 'Opening':
        return ip.opening(image, param_values.get('Kernel Size'))
    elif selected_process == 'Closing':
        return ip.closing(image, param_values.get('Kernel Size'))
    elif selected_process == 'Adaptive thresholding':
        return ip.adaptive_thresholding(image, param_values.get('Type'), param_values.get('Tile size'))
    elif selected_process == 'K means clustering':
        return ip.k_means_clustering(image, param_values.get("K clusters"))


    # Add more operations as needed
