#!/usr/bin/python3
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

import colorDetection as PROCESS  

def show_images(images,text,MODE):          
  # Show the frame
  cv2.putText(images[MODE], "%s:%s" %(MODE,text[MODE]), (10,20),
              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
  cv2.imshow("Frame", images[MODE])

def begin_capture():
  # Initialize the camera and grab a reference to the raw camera capture
  camera = PiCamera()
  camera.resolution = (640, 480)
  camera.framerate = 50
  camera.hflip = True

  rawCapture = PiRGBArray(camera, size=(640, 480))
 
  # Allow the camera to warmup
  time.sleep(0.1)
  print("Starting camera...")
  MODE=0
  
  # Capture frames from the camera
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Capture any key presses
    key = cv2.waitKey(1) & 0xFF
 
    # Grab the raw NumPy array representing the image
    images, text = PROCESS.process_image(frame.array,key)

    # Change display mode or quit
    if key == ord("m"):
      MODE=(MODE+1)%len(images)
    elif key == ord("q"):
      # Only works when running from the terminal
      print("Quit") 
      break

  # Display the output images
    show_images(images,text,MODE)

  # Clear the stream in preparation for the next frame
    rawCapture.truncate(0)

begin_capture()
# End