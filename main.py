# TODO: UNCOMMENT
# from eval import TextLocator
import cv_modules.testInterrupt as ti
# import cv_modules.roi as roi
import contrast 
import cv2
from cv_modules.testInterrupt import ZOOM_MODE, BRIGHTNESS_MODE, CONTRAST_MODE
import config
# from eval import TextLocator

# img2 = textlocator.findtext(img)


def update_image(img):
    # CHANGE FUNCTION TO DNAIELS
    img = zoom(config.level_horz, config.level_vert, config.level_zoom, img.copy())

    img_to_disp = changeContrastBrightness(img, config.level_contrast, config.level_brightness)

    cv2.imshow("Capturing", img_to_disp)
    return img

if __name__ == '__main__':
    ti.setup_GPIO()

    ti.enable_int()
    # TODO: uncomment
    # new_locator = TextLocator()    
    # webcam = cv2.VideoCapture(0) 
    img_held_f = False
    img = None          # process
    original = None
    print("initialised in view finger")
    while True:

        if config.camera_mode == config.VIEWFINDERMODE:
            # TODO: uncomment
            # check, frame = webcam.read()

            # viewfinder mode
            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd 
            # cv2.imshow("Capturing", frame)
            img_held_f = False
       
        elif config.camera_mode == config.EDITMODE:
            if img_held_f == False:
                # TODO: uncomment
                # check, frame = webcam.read()

                # img = frame
                # original = frame.copy()
                print("holding image")
                img_held_f = True
            
            if config.image_edited:
                # TODO: Uncomment and comment prints
                # update alles
                # img = update_image(original)
                print(config.level_brightness)
                print(config.level_contrast)
                print(config.level_horz)
                print(config.level_vert)
                print(config.level_zoom)
                config.image_edited = False
                pass
        
        if config.process_img:
            # TODO: UNCOMMENT
            # new_img = new_locator.findtext(img)
            # cv2.imshow("Capturing", new_img)
            print("Image being processed")
            config.process_img = False
            

       
