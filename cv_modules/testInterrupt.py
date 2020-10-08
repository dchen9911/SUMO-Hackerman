import RPi.GPIO as GPIO
import time

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
    global camera_flag
    camera_flag = 1
    print(GPIO.input(channel))

# Mode callback
def mode_cb(channel):
    print("MODE: Rising edge detected")
    global mode_flag
    if mode_flag == 0:
        mode_flag == 1
    if mode_flag == 1:
        mode_flag == 2
    if mode_flag == 2:
        mode_flag== 3
    if mode_flag == 3:
        mode_flag == 0
    print(GPIO.input(channel))

# DP Up callback
def dpup_cb(channel):
    print("DPAD UP: Rising edge detected")
    global dpup_flag
    dpup_flag = 1
    print(GPIO.input(channel))

# DP Down callback
def dpdown_cb(channel):
    print("DPAD Down: Rising edge detected")
    global dpdown_flag
    dpdown_flag = 1
    print(GPIO.input(channel))

# DP Left callback
def dpleft_cb(channel):
    print("DPAD Left: Rising edge detected")
    global dpleft_flag
    dpleft_flag = 1
    print(GPIO.input(channel))

# DP Up callback
def dpright_cb(channel):
    print("DPAD Right: Rising edge detected")
    global dpright_flag
    dpright_flag = 1
    print(GPIO.input(channel))

# Toggle callback
def toggle_cb(channel):
    print("TOGGLE: Rising edge detected")
    global toggle_flag
    toggle_flag = 1
    print(GPIO.input(channel))
    
def button_cb(channel):
    print("Button callback")
    if channel == BUTTON:
        global pan_left
        if GPIO.input(channel):
            pan_left = 1
        else:
            pan_left = 0
        GPIO.output(OUTPUT, GPIO.input(channel))
            

            
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

