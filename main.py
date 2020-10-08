from eval import TextLocator
import cv_modules.testInterrupt as ti
# import cv_modules.roi as roi
import contrast 
import cv2
from cv_modules.testInterrupt import ZOOM_MODE, BRIGHTNESS_MODE, CONTRAST_MODE

# from eval import TextLocator

# img2 = textlocator.findtext(img)




camera_flag = 0      # triggers the camera to freeze/
mode_flag = ZOOM_MODE      # change the mode
dpup_flag = 0       # dpad up 
dpdown_flag = 0     # dpad down
dpleft_flag = 0     # dpad left
dpright_flag = 0    # dpad right
toggle_flag = 0     # toggles between using the dpad as a pan or as part of mode



if __name__ == '__main__':

    ti.enable_int()
    new_locator = TextLocator()

    cam = cv2.VideoCapture(0) 
    while True:

        level_zoom = 0
        level_contrast = 0
        level_brightness = 0

        # viewfinder mode
        check, frame = webcam.read()
        # print(check) #prints true as long as the webcam is running
        # print(frame) #prints matrix values of each framecd 
        cv2.imshow("Capturing", frame)

        if camera_flag:

            img = frame
            original = frame.copy()

            camera_flag = 0
            overlayed_img = new_locator.fastLocateText(img.copy())
            cv2.imshow("Capturing", overlayed_img)
            #  editing mode
            while not camera_flag:
                
                # toggle dpad as movement or characteristic
                if toggle_flag == 1:

                    # when on zoom, dpad
                    if mode_flag == ZOOM_MODE:
                        # DPAD
                        if dpup_flag == 1:
                            # zoom in

                        if dpdown_flag == 1:
                            # zoom out

                        if dpleft_flag == 1:

                        if dpright_flag == 1:
                            new_locator.()
                            dpright_flag = 0

                    else if mode_flag == CONTRAST_MODE:
                        # contrast

                        img_name = '1'

                        img_path = 'tmp/'+ img_name + '.jpg'
                        info_path = 'tmp/' + img_name + '.txt'

                        img = cv2.imread(img_path)
                        img2 = im.open(img_path) 
                        img3 = im2

                        # content
                        if dpup_flag == 1:
                            level_contrast += 10
                            
                            changeContrastBrightness(img2, level_contrast, level_brightness)

                            display_image(img2)
                            dpup_flag = 0
                        
                        if dpright_flag == 1:
                            # process image

                        if dpdown_flag == 1:
                            level_contrast -= 10
                            
                            changeContrastBrightness(img2, level_contrast, level_brightness)

                            display_image(img2)
                            dpdown_flag = 0

                        if dpleft_flag == 1:
                            # back to viewfinder
                    
                    else if mode_flag == BRIGHTNESS_MODE:
                    # brightness
                        # content
                        if dpup_flag == 1:
                            level_brightness += 10
                            
                            changeContrastBrightness(img2, level_contrast, level_brightness)

                            display_image(img2)
                            dpup_flag = 0
                        
                        if dpright_flag == 1:
                            # process image

                        if dpdown_flag == 1:
                            level_brightness -= 10
                            
                            changeContrastBrightness(img2, level_contrast, level_brightness)

                            display_image(img2)
                            dpdown_flag = 0

                        if dpleft_flag == 1:
                            # back to viewfinder
                    
                    toggle_flag = 0

                else if toggle_flag == 0:
                    # dpad as pan

            # reset flag after leaving editing mode
            camera_flag = 0
                



        

