# import ocr_tesseract as ocr
# import cv_modules.testInterrupt as ti
# import cv_modules.roi as roi
import contrast 

# from eval import TextLocator

# img2 = textlocator.findtext(img)

global pan_left

global camera_flag
global mode_flag
global dpup_flag
global dpdown_flag
global dpleft_flag
global dpright_flag
global toggle_flag

if __name__ == '__main__':

    level_zoom = 0
    level_contrast = 0
    level_brightness = 0

    ti.enable_int()

    while True:
        # if 
        if camera_flag:
            
            # get the image from the camera

        # toggle dpad as movement or characteristic
        if toggle_flag == 1:

            # when on zoom, dpad
            if mode_flag == 1:
                # DPAD
                if dpup_flag == 1:
                    

                if dpdown_flag == 1:
                    
                if dpleft_flag == 1:

                if dpright_flag == 1:
                # dpad as pan

            else if mode_flag == 2:
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
                    level_contrast += 10
                    
                    changeContrastBrightness(img2, level_contrast, level_brightness)

                    display_image(img2)
                    dpright_flag = 0

                if dpdown_flag == 1:
                    level_contrast -= 10
                    
                    changeContrastBrightness(img2, level_contrast, level_brightness)

                    display_image(img2)
                    dpdown_flag = 0

                if dpleft_flag == 1:
                    level_contrast -= 10
                    
                    changeContrastBrightness(img2, level_contrast, level_brightness)

                    display_image(img2)
                    dpleft_flag = 0
            
            else if mode_flag == 3:
            # brightness
                # content
                if dpup_flag == 1:
                    level_brightness += 10
                    
                    changeContrastBrightness(img2, level_contrast, level_brightness)

                    display_image(img2)
                    dpup_flag = 0
                
                if dpright_flag == 1:
                    level_brightness += 10
                    
                    changeContrastBrightness(img2, level_contrast, level_brightness)

                    display_image(img2)
                    dpright_flag = 0

                if dpdown_flag == 1:
                    level_brightness -= 10
                    
                    changeContrastBrightness(img2, level_contrast, level_brightness)

                    display_image(img2)
                    dpdown_flag = 0

                if dpleft_flag == 1:
                    level_brightness -= 10
                    
                    changeContrastBrightness(img2, level_contrast, level_brightness)

                    display_image(img2)
                    dpleft_flag = 0

        else if toggle_flag == 1:
            # dpad as mode

        # switch mode and set led
        if mode_flag == 1:
            # zoom

        else if mode_flag == 2:


        else if mode_flag == 3:
            # brightness
        



        

