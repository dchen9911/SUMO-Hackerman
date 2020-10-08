# TODO: image preprocessing on warped output to get better OCR performance
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from scipy.ndimage import interpolation as inter

import shutil
import os
import glob

# img contains the image data
# coords_str is a string of 8 comma separated coordinates, 4 * (x,y) coordinates)
# returns coords, the original coordinates and the flattened region
def crop_rotated_rect(img, coords_str, debug=False):
    coords = []
    split_coords_str =  coords_str.strip().split(',')
    for i in range(int(len(split_coords_str)/2)):
        coord = [[int(split_coords_str[2*i]), int(split_coords_str[2*i + 1])]]
        coords.append(coord)
    cnt = np.array(coords)

    # print("shape of cnt: {}".format(cnt.shape))
    rect = cv2.minAreaRect(cnt)
    # print("rect: {}".format(rect))

    # the order of the box points: bottom left, top left, top right,
    # bottom right
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    print("bounding box: {}".format(box))
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    # get width and height of the detected rectangle
    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    # coordinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    flat_rect = cv2.warpPerspective(img, M, (width, height))
    if debug:
        cv2.imshow('image', flat_rect)
        cv2.waitKey(0)

    im_h, im_w , _ = flat_rect.shape
    print("Width {}, height: {}".format(im_w, im_h))
    # this means text is vertical
    if im_h > 2*im_w:
        # rotated by 90 deg
        flat_rect = flat_rect.swapaxes(0,1)[::-1,:,:]
        if debug:
            cv2.imshow('image', flat_rect)
            cv2.waitKey(0)

    return coords, flat_rect

# make the image black and white, get rid of noise text thick
def process_for_OCR(imgf, debug=False):
    if debug:
        cv2.imshow('image', imgf)
        cv2.waitKey(0)

    #noise removal
    #decoloring noise using non local means
    imgf = cv2.fastNlMeansDenoisingColored(imgf, None, 10, 10, 7, 21)
    if debug:
        cv2.imshow('image', imgf)
        cv2.waitKey(0)

    # applies gaussian blur
    imgf = cv2.GaussianBlur(imgf, (3,3), 0)
    if debug:
        cv2.imshow('image', imgf)
        cv2.waitKey(0)

    # # turns image greyscale
    # imgf = cv2.cvtColor(imgf, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('image', imgf)
    # cv2.waitKey(0)

    # # binirisation
    # # adaptive gaussian binzrisation threshold
    # imgf = cv2.adaptiveThreshold(imgf,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2) #imgf contains Binary image
    # cv2.imshow('image', imgf)
    # cv2.waitKey(0)

    # Thinning and skeletonising 
    # using erode and dilate
    kernel = np.ones((3,3),np.uint8)
    imgf = cv2.dilate(imgf,kernel,iterations=1)
    imgf = cv2.erode(imgf,kernel,iterations=1)
    if debug:
        cv2.imshow('image', imgf)
        cv2.waitKey(0)

    # # changes back to color image
    # imgf = cv2.cvtColor(imgf, cv2.COLOR_GRAY2BGR)
    # cv2.imshow('image', imgf)
    # cv2.waitKey(0)

    return imgf

class TextRecogniser:
    def __init__(self):
        #configuration setting to convert image to string.  
        self.configuration = ("-l eng --oem 1 --psm 8")

    def recogniseText(self, orig_im, im_to_disp, coords_strs):

        for line in coords_strs:
            coords_str = line.strip()

            coords, flat_rect = crop_rotated_rect(orig_im, coords_str)
            flat_rect = process_for_OCR(flat_rect, debug=False)

            # convert from bgr to rgb
            flat_rect = cv2.cvtColor(flat_rect, cv2.COLOR_BGR2RGB)

            # This will recognize the text from flattened bounding box
            text = pytesseract.image_to_string(flat_rect, config=self.configuration)
            print("{}".format(text))        

            # only add text if the character is english
            text_to_add = "".join([x if ord(x) < 128 else "" for x in text]).strip()
            # print(coords)
            cv2.putText(im_to_disp, text_to_add, (coords[0][0][0], coords[0][0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0, 255), 5)
        return im_to_disp
        # im_to_disp = cv2.cvtColor(im_to_disp, cv2.COLOR_BGR2RGB)
        # plt.imshow(im_to_disp)
        # plt.show()


def main():
    in_folder = 'test_images/'
    out_folder = 'output_ims/'
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    fpaths = glob.glob(in_folder + '*.jpg')

    for i, filepath in enumerate(fpaths):
        filename = filepath.split('/')[-1]

        img_name = filename.split('.')[0]
        
        img_path = in_folder + img_name + '.jpg'
        info_path = out_folder + img_name + '.txt'

        out_img_path = out_folder+ img_name +  '_text' + '.jpg'
        out_info_path = out_folder + img_name + '_text' + '.txt'

        img = cv2.imread(img_path)

        img_to_disp = cv2.imread(out_folder+ img_name + '.jpg')

        #configuration setting to convert image to string.  
        configuration = ("-l eng --oem 1 --psm 8")

        # points for test.jpg
        if os.path.exists(info_path):
            f = open(info_path, 'r')
        else:
            print("Img {} has no text".format(img_name))

        all_coords = []
        all_texts = []

        f_out = open(out_info_path, 'w+')
        for line in f.readlines():
            coords_str = line.strip()

            coords, flat_rect = crop_rotated_rect(img, coords_str)
            flat_rect = process_for_OCR(flat_rect, debug=False)

            # convert from bgr to rgb
            flat_rect = cv2.cvtColor(flat_rect, cv2.COLOR_BGR2RGB)

            # This will recognize the text from flattened bounding box
            text = pytesseract.image_to_string(flat_rect, config=configuration)
            f_out.write("{}\n".format(text))        

            # only add text if the character is english
            text_to_add = "".join([x if ord(x) < 128 else "" for x in text]).strip()
            # print(coords)
            cv2.putText(img_to_disp, text_to_add, (coords[0][0][0], coords[0][0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0, 255), 5)
            cv2.imwrite(out_img_path, img_to_disp) 
        
        img_to_disp = cv2.cvtColor(img_to_disp, cv2.COLOR_BGR2RGB)
        # plt.imshow(img_to_disp)
        # plt.show()
        f_out.close()

if __name__ == "__main__":
    pass