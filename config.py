from cv_modules.testInterrupt import ZOOM_MODE, BRIGHTNESS_MODE, CONTRAST_MODE

VIEWFINDERMODE = 0
EDITMODE = 1
INTERPRETMODE = 2

camera_mode = VIEWFINDERMODE

level_horz = 0
level_vert = 0
level_zoom = 0
level_contrast = 0
level_brightness = 0

image_edited = False

process_img = False
img_fast_f = False


mode_flag = ZOOM_MODE      # change the mode
prev_mode = ZOOM_MODE
