from . import imageProcessing as ip
def Apply(image, selected_process):
    if selected_process== 'Blur':
         return ip.blur(image)
    
    elif selected_process== 'Sharpen':
        return ip.sharpen(image)

    elif(selected_process)== 'Median':
        return ip.median(image)

    elif(selected_process)== 'Grayscale':
        return ip.grayscale(image)
    
    elif(selected_process)== 'Invert':
        return ip.invert(image)

    elif(selected_process)== 'Threshold':
        return ip.threshold(image)


    