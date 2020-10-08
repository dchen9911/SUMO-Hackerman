PAN_MODE = 0
ZOOM_MODE = 1
CONTRAST_MODE = 2
BRIGHTNESS_MODE = 3

import RPi.GPIO as GPIO
import time
import config

#  NEED TO CHANGE PINS
BUTCAMERA = 0
BUTMODE = 12
BUTDPUP = 5
BUTDPDOWN = 6
BUTDPLEFT = 13
BUTDPRIGHT = 19
BUTTOGGLE = 16

BUTLED1 = 5
BUTLED2 = 4

# Inputs
TOGGLE = 29
BUTTON = 31

OUTPUT = 33

# GPIO.setmode(GPIO.BOARD)

# GPIO.setup(TOGGLE, GPIO.IN)
# GPIO.setup(BUTTON, GPIO.IN)

# GPIO.setup(OUTPUT, GPIO.OUT)

pan_left = 0
pan_right = 0

# time.sleep(0.1)

def setup_GPIO():
    GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
    GPIO.setup(BUTDPUP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     
    GPIO.setup(BUTDPDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     
    GPIO.setup(BUTDPLEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     
    GPIO.setup(BUTDPRIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     
    GPIO.setup(BUTTOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(BUTCAMERA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BUTMODE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  
def enable_int():
    # camera
    GPIO.add_event_detect(BUTCAMERA, GPIO.FALLING, callback=camera_cb, bouncetime=200)

    # mode
    GPIO.add_event_detect(BUTMODE, GPIO.FALLING, callback=mode_cb, bouncetime=200)

    # dpup
    GPIO.add_event_detect(BUTDPUP, GPIO.FALLING, callback=dpup_cb, bouncetime=200)

    # dpdown
    GPIO.add_event_detect(BUTDPDOWN, GPIO.FALLING, callback=dpdown_cb, bouncetime=200)

    # dpleft
    GPIO.add_event_detect(BUTDPLEFT, GPIO.FALLING, callback=dpleft_cb, bouncetime=200)

    # dpright
    GPIO.add_event_detect(BUTDPRIGHT, GPIO.FALLING, callback=dpright_cb, bouncetime=200)

    # toggle
    GPIO.add_event_detect(BUTTOGGLE, GPIO.FALLING, callback=toggle_cb, bouncetime=200)

    # GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=button_cb, bouncetime=200)

def disable_int():
    GPIO.remove_event_detect(BUTCAMERA)
    GPIO.remove_event_detect(BUTMODE)
    GPIO.remove_event_detect(BUTDPDOWN)
    GPIO.remove_event_detect(BUTDPLEFT)
    GPIO.remove_event_detect(BUTDPRIGHT)
    GPIO.remove_event_detect(BUTDPUP)
    GPIO.remove_event_detect(BUTTOGGLE)

# Camera callback
def camera_cb(channel):
    print("CAMERA: Rising edge detected")
    
    config.camera_mode = not config.camera_mode
    if (config.camera_mode == config.VIEWFINDERMODE):
        print("Just switched to viewfinder mode")
    elif (config.camera_mode == config.EDITMODE):
        print("Just switched to edit mode")
    else:
        print("WE screwd up switching modes")
    print(GPIO.input(channel))

# Mode callback
def mode_cb(channel):
    print("MODE: Rising edge detected")
    
    if config.mode_flag == ZOOM_MODE:
        config.mode_flag = CONTRAST_MODE
        print("Switched to contrast mode")
    elif config.mode_flag == CONTRAST_MODE:
        config.mode_flag = BRIGHTNESS_MODE
        print("Switched to brightness mode")
    elif config.mode_flag == BRIGHTNESS_MODE:
        config.mode_flag = ZOOM_MODE
        print("Switched to zoom mode")

    print(GPIO.input(channel))

# DP Up callback
def dpup_cb(channel):
    print("DPAD UP: Rising edge detected")
    print(GPIO.input(channel))

    if config.camera_mode == config.EDITMODE:
        if config.mode_flag == PAN_MODE:
            config.level_vert += 10
        if config.mode_flag == ZOOM_MODE:
            config.level_zoom += 10
        elif config.mode_flag == CONTRAST_MODE:
            config.level_contrast += 10
        elif config.mode_flag == BRIGHTNESS_MODE:
            config.level_brightness += 10
        config.image_edited = True


# DP Down callback
def dpdown_cb(channel):
    print("DPAD Down: Rising edge detected")
    print(GPIO.input(channel))
    if config.camera_mode == config.EDITMODE:
        if config.mode_flag == PAN_MODE:
            config.level_vert -= 10
        elif config.mode_flag == ZOOM_MODE:
            config.level_zoom -= 10
        elif config.mode_flag == CONTRAST_MODE:
            config.level_contrast -= 10
        elif config.mode_flag == BRIGHTNESS_MODE:
            config.level_brightness -= 10

        config.image_edited = True
    

# DP Left callback
def dpleft_cb(channel):
    print("DPAD Left: Rising edge detected")
    print(GPIO.input(channel))
    if config.camera_mode == config.EDITMODE:
        if config.mode_flag == PAN_MODE:
            config.level_horz -= 10
            config.image_edited = True

        else:
            config.camera_mode = config.VIEWFINDERMODE
            print("switch back to viewfinder")
    elif config.camera_mode == config.INTERPRETMODE:
        print
        config.cycle -= 1
        # trigger next next
        pass
        

# DP Up callback
def dpright_cb(channel):
    print("DPAD Right: Rising edge detected")
    print(GPIO.input(channel))
    if config.camera_mode == config.EDITMODE:
        if config.mode_flag == PAN_MODE:
            config.level_horz += 10
            config.image_edited = True
        elif config.camera_mode == config.EDITMODE:
            print("img fast f mode", config.img_fast_f)
            if config.img_fast_f == False:
                config.img_fast_f = True
                config.image_edited = True
            else:
                config.process_img = True
                config.img_fast_f = False
    elif config.camera_mode == config.INTERPRETMODE:
        print("going to interpret mode")
        config.cycle += 1
        # trigger next next
        pass

# Toggle callback
def toggle_cb(channel):
    print("TOGGLE: Rising edge detected")
    print(GPIO.input(channel))  

    if config.camera_mode == config.EDITMODE:
        if config.mode_flag != PAN_MODE:
            config.prev_mode = config.mode_flag
            config.mode_flag = PAN_MODE
        else:
            config.mode_flag = config.prev_mode

           

            
if __name__ == "__main__":
    
    input("Press Enter when ready \n")

    enable_int()

    count = 0
    while(True):
        if pan_left:
            count = count + 1
            time.sleep(0.2)
            
        #else:
            #print(count)

