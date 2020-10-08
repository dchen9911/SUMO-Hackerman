# TODO: UNCOMMENT
# from eval import TextLocator
import cv_modules.testInterrupt as ti
# import cv_modules.roi as roi
from contrast import changeContrastBrightness 
import cv2
from cv_modules.testInterrupt import ZOOM_MODE, BRIGHTNESS_MODE, CONTRAST_MODE
from cv_modules.zoom import zoom
import config
# from eval import TextLocator

# img2 = textlocator.findtext(img)


def update_image(img):
    # CHANGE FUNCTION TO DNAIELS
    img = zoom(config.level_horz, config.level_vert, config.level_zoom, img)

    img_to_disp = changeContrastBrightness(img, config.level_contrast, config.level_brightness)

    cv2.imshow("Capturing", img_to_disp)
    cv2.waitKey(1000)
    return img_to_disp

if __name__ == '__main__':
    ti.setup_GPIO()

    ti.enable_int()
    # TODO: uncomment
    # new_locator = TextLocator() 
    #    
    webcam = cv2.VideoCapture(0) 
    img_held_f = False
    config.img_fast_f = False
    img = None          # process
    original = None
    print("initialised in view finger")
    while True:

        if config.camera_mode == config.VIEWFINDERMODE:

            config.level_vert = 0
            config.level_horz = 0
            config.level_zoom = 0
            config.level_contrast = 0
            config.level_brightness = 0

            check, frame = webcam.read()
           
            # dispaly it for 1 ms
            cv2.waitKey(1)
            # viewfinder mode
            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd 
            cv2.imshow("Capturing", frame)
            img_held_f = False
       
        elif config.camera_mode == config.EDITMODE:
            if img_held_f == False:

                img = frame
                original = frame.copy()
                print("holding image")

                img_held_f = True
            
            if config.image_edited:
                # update all things
                print("Updating the image)")
                img = update_image(original.copy())
                
                if config.img_fast_f == True:
                    print("show fast img")
                    # fast_img = new_locator.fastLocateText(img.copy())
                print('brigtness: ' + str(config.level_brightness)) 
                print('contrast: ' + str(config.level_contrast))
                print('level_horz: ' +str( config.level_horz))
                print('level_vert: ' +str( config.level_vert))
                print('level_zoom: ' +str( config.level_zoom))
                config.image_edited = False
                pass

        elif config.camera_mode == config.INTERPRETMODE:
            # print('switch to interpret mode')

            if config.cycle > config.cycle_prev:
                # img = getNext(img.copy())
                print(config.cycle, config.cycle_prev)
                config.cycle_prev = config.cycle
            elif config.cycle < config.cycle_prev:                
                # img = getPrev(img.copy())
                print(config.cycle, config.cycle_prev)
                config.cycle_prev = config.cycle

            # pass

        
        if config.process_img:
            # TODO: UNCOMMENT
            # new_img = new_locator.findtext(img)
            # cv2.imshow("Capturing", new_img)
            print("Image being processed")
            config.process_img = False
            config.camera_mode = config.INTERPRETMODE
            

       
