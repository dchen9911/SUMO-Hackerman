import cv2
import numpy as np
import argparse

# img = cv2.imread("./cv_modules/1.jpg")
# original_img = img
# cv2.imshow("Original", img)
# cv2.imshow('img', img)
# cv2.waitKey(0)



# 0-100 relative to full size. 100 is max. 
# -100 to 100 
# horz, vert, zoom, image

# Define max zoom to be a zoom of 20x. E.g. at 20x zoom, the zoomed 
# image will be composed of 5% of the original image, blown up.
def zoom(horz, vert, zoom, img):
    dims = img.shape
    width = dims[1]
    height = dims[0]

    if horz > 100:
        horz = 100
    elif horz < -100:
        horz = -100

    if vert > 100:
        vert = 100
    elif vert < -100:
        vert = -100

    if zoom > 100:
        zoom = 100
    elif zoom < 0:
        zoom = 0

    horzInc = width/200
    vertInc = height/200

    # Scaling factor calculated from requested zoom
    scale = 1 - 0.95*zoom/100

    cropWidth = int(width*scale)
    cropHeight =  int(height*scale)

    minX = int((horz + 100) * horzInc - cropWidth/2)
    minY = int((vert + 100) * vertInc - cropHeight/2)
    maxX = int((horz + 100) * horzInc + cropWidth/2)
    maxY = int((vert + 100) * vertInc + cropHeight/2)

    # Check to make sure desired box doesn't go out of bounds
    if minY < 0 and minX < 0:
        croppedImg = img[0:cropHeight, 0:cropWidth]
    elif minY < 0 and maxX > width: 
        croppedImg = img[0:cropHeight, width - cropWidth : width]
    elif maxY > height and minX < 0:
        croppedImg = img[height - cropHeight : height, 0:cropWidth]
    elif maxX > height and maxX > width:
        croppedImg = img[height - cropHeight : height, width - cropWidth : width]

    elif minY < 0:
        croppedImg = img[0:cropHeight, minX:maxX]
    elif maxY > height:
        croppedImg = img[height - cropHeight : height, minX:maxX]
    elif minX < 0:
        croppedImg = img[minY:maxY, 0:cropWidth]
    elif maxX > width: 
        croppedImg = img[minY:maxY, width - cropWidth : width]    

    else:
        croppedImg = img[minY:maxY, minX:maxX]

    # Zoom into the cropped image 
    zoomedImg = cv2.resize(croppedImg, (dims[1], dims[0]), interpolation=cv2.INTER_AREA)

    return zoomedImg

zoomed = zoom(95, 95, 110, img)
cv2.imshow('Zoomed', zoomed)
cv2.waitKey(0)