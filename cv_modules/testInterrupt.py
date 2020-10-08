import RPi.GPIO as GPIO
import time

PAN_MODE = 0
ZOOM_MODE = 1
CONTRAST_MODE = 2
BRIGHTNESS_MODE = 3

#  NEED TO CHANGE PINS
BUTCAMERA = 1
BUTMODE = 2
BUTLED1 = 3
BUTLED2 = 4
BUTDPUP = 5
BUTDPDOWN = 6
BUTDPLEFT = 7
BUTDPRIGHT = 8
BUTTOGGLE = 9

# Inputs
TOGGLE = 29
BUTTON = 31

OUTPUT = 33

GPIO.setmode(GPIO.BOARD)

GPIO.setup(TOGGLE, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN)

GPIO.setup(OUTPUT, GPIO.OUT)

pan_left = 0
pan_right = 0

# time.sleep(0.1)

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


    GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=button_cb, bouncetime=200)

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
    
    camera_mode = not camera_mode

    print(GPIO.input(channel))

# Mode callback
def mode_cb(channel):
    print("MODE: Rising edge detected")
    global mode_flag
    
    if mode_flag == ZOOM_MODE:
        mode_flag == CONTRAST_MODE
    if mode_flag == CONTRAST_MODE:
        mode_flag== BRIGHTNESS_MODE
    if mode_flag == BRIGHTNESS_MODE:
        mode_flag == ZOOM_MODE
    print(GPIO.input(channel))

# DP Up callback
def dpup_cb(channel):
    print("DPAD UP: Rising edge detected")

    if mode_flag == PAN_MODE:
        level_vert += 10
    if mode_flag == ZOOM_MODE:
        level_zoom += 10
    elif mode_flag == CONTRAST_MODE:
        level_contrast += 10
    elif mode_flag == BRIGHTNESS_MODE:
        level_brightness += 10
    image_edited = True

    print(GPIO.input(channel))

# DP Down callback
def dpdown_cb(channel):
    print("DPAD Down: Rising edge detected")
    if mode_flag == PAN_MODE:
        level_vert -= 10
    elif mode_flag == ZOOM_MODE:
        level_zoom -= 10
    elif mode_flag == CONTRAST_MODE:
        level_contrast -= 10
    elif mode_flag == BRIGHTNESS_MODE:
        level_brightness -= 10

    image_edited = True
    print(GPIO.input(channel))

# DP Left callback
def dpleft_cb(channel):
    print("DPAD Left: Rising edge detected")
    if mode_flag == PAN_MODE:
        level_horz -= 10
        image_edited = True

    else
        camera_mode = VIEWFINDERMODE
    print(GPIO.input(channel))

# DP Up callback
def dpright_cb(channel):
    print("DPAD Right: Rising edge detected")
    if mode_flag == PAN_MODE:
        level_horz += 10
        image_edited = True
    else:
        process_img = True
    print(GPIO.input(channel))

# Toggle callback
def toggle_cb(channel):
    print("TOGGLE: Rising edge detected")

    if mode_flag != PAN_MODE:
        prev_mode = mode_flag
        mode_flag = PAN_MODE
    else:
        mode_flag = prev_mode

    print(GPIO.input(channel))         

            
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

