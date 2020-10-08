import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pytesseract
from PIL import Image as im
from PIL import ImageEnhance
from scipy.ndimage import interpolation as inter
from scipy.ndimage import zoom 

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class image_modifier():
    def __init__(self, img, contrast, zoom):
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
        factor = (255 * (level+255)) / (255 * (255-level))
        def contrast(c):
            return 128 + factor * (c - 128)
        self.img = self.img.point(contrast)
    
    def display_image(self):
        # cv2.imshow('image', self.img)
        # cv2.waitKey(0)

        plt.imshow(self.img)
        plt.title('Output')
        plt.show()

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

    # cannot have number >=255 and <-255 is pure grey
    imgHandler.change_contrast(-200)
    imgHandler.display_image()

    # change zoom
    imgHandler.change_zoom(1.5)


    #configuration setting to convert image to string.  
    configuration = ("-l eng --oem 1 --psm 8")

    # points for test.jpg
    f = open(info_path, 'r')
    
    plt.imshow(imgHandler.img)
    plt.title('Output')
    plt.show()