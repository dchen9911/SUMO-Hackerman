from eval import TextLocator
import cv_modules.testInterrupt as ti
# import cv_modules.roi as roi
import contrast 
import cv2
from cv_modules.testInterrupt import ZOOM_MODE, BRIGHTNESS_MODE, CONTRAST_MODE

# from eval import TextLocator

# img2 = textlocator.findtext(img)

VIEWFINDERMODE = 0
EDITMODE = 1

camera_mode = VIEWFINDERMODE

level_horz = 0
level_vert = 0
level_zoom = 0
level_contrast = 0
level_brightness = 0

image_edited = False

process_img = False


mode_flag = ZOOM_MODE      # change the mode
prev_mode = ZOOM_MODE


def update_image(img):
    # CHANGE FUNCTION TO DNAIELS
    img = zoom(level_horz, level_vert, level_zoom, original.copy())

    img_to_disp = changeContrastBrightness(img, level_contrast, level_brightness)
    cv2.imshow("Capturing", img_to_disp)
    return img

if __name__ == '__main__':

    ti.enable_int()
    new_locator = TextLocator()

    cam = cv2.VideoCapture(0) 
    img_held_f = False
    img = None          # process
    original = None
    while True:

        if camera_mode == VIEWFINDERMODE:
            check, frame = webcam.read()

            # viewfinder mode
            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd 
            cv2.imshow("Capturing", frame)
            img_held_f = False
       
        elif camera_mode == EDITMODE:
            if img_held_f == False:
                check, frame = webcam.read()

                img = frame
                original = frame.copy()
                img_held_f = True
            
            if image_edited:
                # update alles
                img = update_image(img)
                image_edited = False
                pass
        
        if process_img:
            new_img = new_locator.findtext(img)
            cv2.imshow("Capturing", new_img)
            process_img = False
            

       