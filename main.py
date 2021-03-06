from eval import TextLocator
import cv_modules.testInterrupt as ti
from contrast import changeContrastBrightness 
import cv2
from cv_modules.testInterrupt import ZOOM_MODE, BRIGHTNESS_MODE, CONTRAST_MODE
from cv_modules.zoom import zoom
from cv_modules.roi import click_and_crop_cb, checkROI, crop
import config
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1920, 1440)
# camera.framerate = 10



def update_image(img):
    # CHANGE FUNCTION TO DNAIELS
    img = zoom(config.level_horz, config.level_vert, config.level_zoom, img)

    img_to_disp = changeContrastBrightness(img, config.level_contrast, config.level_brightness)

    cv2.imshow("Capturing", img_to_disp)
    cv2.waitKey(1)
    return img_to_disp

if __name__ == '__main__':
    cv2.namedWindow('Capturing', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Capturing', 800, 570)
    cv2.resizeWindow('Capturing', 500, 370)
    
    ti.setup_GPIO()
    ti.enable_int()

    # cv2.setMouseCallback("Capturing", click_and_crop_cb)

    new_locator = TextLocator() 

    # webcam = cv2.VideoCapture(0) 
    img_held_f = False
    config.img_fast_f = False
    img = None          # process
    original = None

    fast_img_disped = False

    print("initialised in view finger")
    while True:

        if config.camera_mode == config.VIEWFINDERMODE:
            fast_img_disped = False
            config.img_fast_f = False
            config.level_vert = 0
            config.level_horz = 0
            config.level_zoom = 0
            config.level_contrast = 0
            config.level_brightness = 0

            # grab capture from camera
            rawCapture = PiRGBArray(camera)
            time.sleep(0.03)

            camera.capture(rawCapture, format="bgr")
            frame = cv2.cvtColor(rawCapture.array, cv2.COLOR_BGR2RGB) 
           
            
            # viewfinder mode
            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd 
            cv2.imshow("Capturing", frame)
            # dispaly it for 1 ms
            cv2.waitKey(10)

            img_held_f = False
        elif config.camera_mode == config.EDITMODE:
            if img_held_f == False:

                img = frame
                original = frame.copy()
                print("holding image")
                print(frame.shape)
                img_held_f = True
            
            if config.image_edited:
                # update all things
                print("Updating the image)")
                if config.img_fast_f == True and fast_img_disped == False:
                    print("show fast img")
                    fast_img = new_locator.fastLocateText(original.copy())
                    img = update_image(fast_img)
                    fast_img_disped = True
                elif config.img_fast_f == True:
                    img = update_image(fast_img.copy())
                else:
                    img = update_image(original.copy())

                
                print('brigtness: ' + str(config.level_brightness)) 
                print('contrast: ' + str(config.level_contrast))
                print('level_horz: ' +str( config.level_horz))
                print('level_vert: ' +str( config.level_vert))
                print('level_zoom: ' +str( config.level_zoom))
                config.image_edited = False
                pass

        elif config.camera_mode == config.INTERPRETMODE:

            if config.cycle > config.cycle_prev:
                print('getting prev word')
                img = new_locator.get_next_word()
                print(config.cycle, config.cycle_prev)
                config.cycle_prev = config.cycle
            elif config.cycle < config.cycle_prev:     
                print('getting next word')           
                img = new_locator.get_prev_word()
                print(config.cycle, config.cycle_prev)
                config.cycle_prev = config.cycle
            cv2.imshow("Capturing", img)
            cv2.waitKey(1)

        # # can only do roi in the edit mode        
        # if config.camera_mode == config.EDITMODE and img is not None:
        #     if config.cropping is True:
        #         print("Doing the cropping")
        #         config.clickCoord, validROI = checkROI(original, config.clickCoord)
        #         if validROI == 1:
        #             img = original.copy()
        #         elif validROI == 2:
        #             print("INTO VALID ROI")
        #             img, img_cropped = crop(img, config.clickCoord)
        #         config.cropping = False
        #         config.clickCoord = [] 
        #         img = changeContrastBrightness(img, config.level_contrast, config.level_brightness)
        #         cv2.imshow("Capturing", img)
        #         cv2.waitKey(1)
        
        if config.process_img:
            print("Image being processed")
            img = new_locator.findText(original.copy())
            cv2.imshow("Capturing", img)
            cv2.waitKey(1)
            fast_img_disped = False
            print("Image finished processing")
            config.process_img = False
            config.camera_mode = config.INTERPRETMODE
            print('switch to interpret mode')
            

       
