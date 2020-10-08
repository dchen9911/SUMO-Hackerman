# TODO: Consider case of vertical text (maybe try rotatating both ways
# apparently the text always goes down, so rotate counter clockwise
# TODO: image preprocessing on warped output to get better OCR performance

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image as im
from scipy.ndimage import interpolation as inter

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# img contains the image data
# coords_str is a string of 8 comma separated coordinates, 4 * (x,y) coordinates)
# returns coords, the original coordinates and the flattened region
def crop_rotated_rect(img, coords_str):
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
    warped = cv2.warpPerspective(img, M, (width, height))
    plt.imshow(warped)
    plt.show()

    # def find_score(arr, angle):
    #     data = inter.rotate(arr, angle, reshape=False, order=0)
    #     hist = np.sum(data, axis=1)
    #     score = np.sum((hist[1:] - hist[:-1]) ** 2)
    #     return hist, score


    # delta = 1
    # limit = 5
    # angles = np.arange(-limit, limit+delta, delta)
    # scores = []
    # for angle in angles:
    #     hist, score = find_score(warped, angle)
    #     scores.append(score)
    # best_score = max(scores)
    # best_angle = angles[scores.index(best_score)]
    # print('Best angle: {}'.format(best_angle))

    # # correct skew
    # data = inter.rotate(warped, best_angle, reshape=False, order=0)
    # img = im.fromarray((255 * data).astype("uint8")).convert("RGB")

    return coords, warped


def boost_contrast(img):
    #-----Converting image to LAB Color model----------------------------------- 
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)

    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8,8))
    cl = clahe.apply(l)

    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl,a,b))

    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final

# make the image black and white, get rid of noise text thick
def process_for_OCR(imgf):
    cv2.imshow('image', imgf)
    cv2.waitKey(0)

    # noise removal
    # decoloring noise using non local means
    imgf = cv2.fastNlMeansDenoisingColored(imgf, None, 10, 10, 7, 21)
    cv2.imshow('image', imgf)
    cv2.waitKey(0)

    # applies gaussian blur
    imgf = cv2.GaussianBlur(imgf, (5,5), 0)
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
    imgf = cv2.erode(imgf,kernel,iterations=1)
    imgf = cv2.dilate(imgf,kernel,iterations=1)
    cv2.imshow('image', imgf)
    cv2.waitKey(0)

    # # changes back to color image
    # imgf = cv2.cvtColor(imgf, cv2.COLOR_GRAY2BGR)
    # cv2.imshow('image', imgf)
    # cv2.waitKey(0)



    return imgf
    # pass
    # return processed_img


if __name__ == "__main__":
    img_name = '001'

    img_path = 'tmp/'+ img_name + '.jpg'
    info_path = 'tmp/' + img_name + '.txt'

    # img.create(rows, cols, CV_8UC1)
    img = cv2.imread(img_path)

    #configuration setting to convert image to string.  
    configuration = ("-l eng --oem 1 --psm 8")

    # points for test.jpg
    f = open(info_path, 'r')

    all_coords = []
    all_texts = []
    for line in f.readlines():
        coords_str = line.strip()

        coords, flat_rect = crop_rotated_rect(img, coords_str)
        flat_rect = process_for_OCR(flat_rect)

        # convert from bgr to rgb
        flat_rect = cv2.cvtColor(flat_rect, cv2.COLOR_BGR2RGB)

        # This will recognize the text from flattened bounding box
        text = pytesseract.image_to_string(flat_rect, config=configuration)
        print("{}\n".format(text))
        

        # only add text if the character is english
        text_to_add = "".join([x if ord(x) < 128 else "" for x in text]).strip()
        print(coords)
        cv2.putText(img, text_to_add, (coords[0][0][0], coords[0][0][1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0, 255), 2)
    
    plt.imshow(img)
    plt.title('Output')
    plt.show()
