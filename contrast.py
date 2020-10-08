import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pytesseract
from PIL import Image as im
from PIL import ImageEnhance
from scipy.ndimage import interpolation as inter
from scipy.ndimage import zoom 
import argparse


pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class image_modifier():
    def __init__(self, img, contrast, zoom):
        self.original_img = img
        self.img = img
        self.contrast = contrast
        self.zoom = zoom
        print("Modifier init")
    
    def boost_contrast(self, contrast):
        #-----Converting image to LAB Color model----------------------------------- 
        lab= cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)

        #-----Splitting the LAB image to different channels-------------------------
        l, a, b = cv2.split(lab)

        #-----Applying CLAHE to L-channel-------------------------------------------
        clahe = cv2.createCLAHE(clipLimit=contrast, tileGridSize=(8,8))
        cl = clahe.apply(l)

        #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
        limg = cv2.merge((cl,a,b))

        #-----Converting image from LAB Color model to RGB model--------------------
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return final

    def change_contrast(self, level):
        # 
        factor = (255 * (level+101)) / (255 * (101-level))
        def contrast(c):
            return 128 + factor * (c - 128)
        self.img = self.original_img.point(contrast)
    
    def display_image(self):
        # cv2.imshow('image', self.img)
        # cv2.waitKey(0)

        plt.imshow(self.img)
        plt.title('Output')
        plt.show()

    def change_brightness(self, level):
        factor = (255 * (level+101)) / (255 * (101-level))
        enhancer = ImageEnhance.Brightness(self.original_img)
        self.img = enhancer.enhance(factor)

    def change_zoom(self, level, **kwargs):
        # convert pil image to np image
        pix = np.array(self.img.getdata()).reshape(self.img.size[0], self.img.size[1], 3)

        # get the height and width of image and then separate rgb of image to do each channel
        h, w = pix.shape[:2]
        zoom_tuple = (level,) * 2 + (1,) * (pix.ndim - 2)

        # Bounding box of the zoomed-in region within the input array
        zh = int(np.round(h / level))
        zw = int(np.round(w / level))
        top = (h - zh) // 2
        left = (w - zw) // 2

        out = zoom(pix[top:top+zh, left:left+zw], zoom_tuple, **kwargs)

        # `out` might still be slightly larger than `img` due to rounding, so
        # trim off any extra pixels at the edges
        trim_top = ((out.shape[0] - h) // 2)
        trim_left = ((out.shape[1] - w) // 2)
        out = out[trim_top:trim_top+h, trim_left:trim_left+w]

        # convert np image to pil image
        self.img = im.fromarray(np.uint8(cm.gist_earth(pix)*255))

    def roi(self):

        # convert from pil to cv2 image
        pil_image = self.img.convert('RGB') 
        open_cv_image = np.array(pil_image) 
        # Convert RGB to BGR 
        img = open_cv_image[:, :, ::-1].copy() 

        clickCoord = []
        cropping = False


        def click_and_crop_cb(event, x, y, flags, params):
            print("IN")
            global clickCoord, cropping

            if event == cv2.EVENT_LBUTTONDOWN:
                clickCoord = [[x,y],]
                cropping = False

            elif event == cv2.EVENT_LBUTTONUP:
                clickCoord.append( [x,y] )
                cropping = True


        def crop(img, clickCoord):
            # Find out the aspect ratio of original image
            dims = img.shape
            height = dims[0]
            width = dims[1]
            ar = width / height
            print(width, height)

            # Dummy ROI coordinates
            minX = clickCoord[0][0]
            minY = clickCoord[0][1]
            maxX = clickCoord[1][0]
            maxY = clickCoord[1][1]

            # Crop out the desired region
            if (maxX - minX) / (maxY - minY) < ar:  # Desired Y > desired X
                correctedWidth = int((maxY - minY) * ar)
                offset = correctedWidth - (maxX - minX)

                # Check that the corrected AR region doesn't go out of frame
                if minX - offset / 2 < 0:
                    croppedImg = img[minY:maxY, 0:correctedWidth]

                elif maxX + offset / 2 > width:
                    croppedImg = img[minY:maxY, width - correctedWidth : width]

                else:
                    croppedImg = img[minY:maxY, int(minX - offset / 2) : int(maxX + offset / 2)]

            else:  # Desired Y > desired X
                correctedHeight = int((maxX - minX) * ar)
                offset = correctedHeight - (maxX - minX)

                # Check that the corrected AR region doesn't go out of frame
                if minY - offset / 2 < 0:
                    croppedImg = img[0:correctedWidth, minX:maxX]

                elif maxY + offset / 2 > height:
                    croppedImg = img[height - correctedHeight : height, minX:maxX]

                else:
                    croppedImg = img[int(minY - offset / 2) : int(maxY + offset / 2), minX:maxX]

            #cv2.imshow("Cropped", croppedImg)
            # cv2.waitKey(0)

            resized = cv2.resize(croppedImg, (dims[1], dims[0]), interpolation=cv2.INTER_AREA)
            print(resized.shape)

            return resized, croppedImg


        cv2.setMouseCallback("img", click_and_crop_cb)


        while True:
            
            cv2.imshow('img', img)
            cv2.waitKey(0)
            #cv2.destroyAllWindows() 
            if cropping is True:
                print("In")
                if len(clickCoord) == 2:
                    #cv2.rectangle(img, clickCoord[0], clickCoord[1], (0, 255, 0), 2)
                    if (clickCoord[0][0]>clickCoord[1][0]) or (clickCoord[0][1]>clickCoord[1][1]):
                        temp = clickCoord[0][0]
                        clickCoord[0][0] = clickCoord[1][0]
                        clickCoord[1][0] = temp
                        temp = clickCoord[0][1]
                        clickCoord[0][1] = clickCoord[1][1]
                        clickCoord[1][1] = temp
                    img, cropped =  crop(img, clickCoord)
                    #print(  len(clickCoord)  )
                clickCoord = []
                cropping = False






if __name__ == "__main__":
    img_name = '1'

    img_path = 'tmp/'+ img_name + '.jpg'
    info_path = 'tmp/' + img_name + '.txt'

    # img.create(rows, cols, CV_8UC1)
    img = cv2.imread(img_path)
    img2 = im.open(img_path) 


    imgHandler = image_modifier(img2, 5,5)
    imgHandler.display_image()
    # imgHandler.boost_contrast(6)
    # imgHandler.display_image()

    imgHandler.change_brightness(99)
    imgHandler.display_image()

    # cannot have number >=255 and <-255 is pure grey
    while True:
        text = input("Contrast Number between : ")
        # if text.is_integer():
        #     print("Error, must be a number between -100 and 100")
        #     continue
        text = int(text)
        if text > 100:
            text = int(input("Error, number needs to be between -100 and 100: "))
        if text < -100:
            text = int(input("Error, number needs to be between -100 and 100: "))
        if text == 0:
            break

        imgHandler.change_contrast(text)
        imgHandler.display_image()

    # change zoom
    # imgHandler.roi()


    #configuration setting to convert image to string.  
    configuration = ("-l eng --oem 1 --psm 8")

    # points for test.jpg
    f = open(info_path, 'r')
    
    plt.imshow(imgHandler.img)
    plt.title('Output')
    plt.show()