import cv2 as cv
import time

# initialize the camera
cam_port = 0

# start timer
start = time.time()

image_number = 0
stop = time.time()

# 1 photo per second loop
while (stop - start < 100):
    stop = time.time()

    cam = cv.VideoCapture(cam_port)    

    # reading the input and saving using the camera:

    result, image = cam.read()
    if result:
        print('Image taken and saved')
        image_name = 'image' + str(image_number) + '.png'
        cv.imwrite(str('./my_images/' + image_name), image)
    # If captured image is corrupted, moving to else part
    else:
	    print("ERROR! No image detected.")
    
    time.sleep(1)
    image_number += 1
