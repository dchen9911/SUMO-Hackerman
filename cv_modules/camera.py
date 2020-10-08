import cv2

key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
captured = False
while True:
    #print(captured)
    key = cv2.waitKey(1)
    print(key>1)
    if captured is False:
        check, frame = webcam.read()
        #print(check) #prints true as long as the webcam is running
        #print(frame) #prints matrix values of each framecd 
        cv2.imshow("Capturing", frame)
        if key >1: 
            check, imgCaptured = webcam.read()
            webcam.release()
            #cv2.waitKey(1000)
            captured = True

    else:  # If captured is true
        cv2.imshow("Captured!", imgCaptured)
        key = cv2.waitKey(0)
        if key >1:
            print("Restarting Camera")
            webcam = cv2.VideoCapture(0)
            captured = False
        
        
    #except(KeyboardInterrupt):
        #print("Turning off camera.")
        #webcam.release()
        #print("Camera off.")
        #print("Program ended.")
        #cv2.destroyAllWindows()
        #break

