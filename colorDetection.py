#!/usr/bin/python3
import cv2
import numpy as np

BLUR=(5,5)

# Default callback function that does nothing
def callback(x):
    pass


# Create GUI container
cv2.namedWindow("Trackbars")
# Add trackbars to the "Trackbars" GUI container
cv2.createTrackbar("B", "Trackbars", 0, 255, callback)
cv2.createTrackbar("G", "Trackbars", 0, 255, callback)
cv2.createTrackbar("R", "Trackbars", 0, 255, callback)

# Create black blank image
colorImage = np.zeros((300, 300, 3), np.uint8)

def process_image(raw_image,control):
  global threshold
  text=[]
  images=[]
  
  bgr = (cv2.getTrackbarPos("B", "Trackbars"), cv2.getTrackbarPos("G", "Trackbars"), cv2.getTrackbarPos("R", "Trackbars"))
  colorImage[:] = bgr
  cv2.imshow("Trackbars", colorImage);
  
  colorText = "R: "+str(bgr[2])+" G:"+str(bgr[1])+" B:"+str(bgr[0])

  #Keep a copy of the raw image
  text.append("Raw Image %s"%colorText)
  text[0] = "R: "+str(bgr[2])+" G:"+str(bgr[1])+" B:"+str(bgr[0])
  images.append(raw_image)
  
  #Blur the raw image
  text.append("with Blur...%s"%colorText)
  images.append(cv2.blur(raw_image, BLUR))
  
  # Function for properly setting the lower/upper bounds
  def setBounds(arr, change):
      for i in range(0, len(arr)):
          if arr[i] + change < 0:
              arr[i] = 0
          elif arr[i] + change > 255:
              arr[i] = 255
          else:
              arr[i] += change
      return arr
    
    
  threshold = 50
  # Set the lower and upper color thresholds
  values = [bgr[0], bgr[1], bgr[2]]
  lower = np.array(setBounds(values[:], -threshold), dtype="uint8")
  upper = np.array(setBounds(values[:], threshold), dtype="uint8")
  # print(values)
  # print("Lower: " + np.array2string(lower))
  # print("Upper: " + np.array2string(upper))

  text.append("with Threshold...%s"%colorText)
  images.append(cv2.inRange(images[-1], lower, upper))

  #Find contours in the threshold image
  text.append("with Contours...%s"%colorText)
  images.append(images[-1].copy())
  contours, hierarchy = cv2.findContours(images[-1], cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  #Display contour and hierarchy details
  if control == ord("i"):
    print("Contour: %s"%contours)
    print("Hierarchy: %s"%hierarchy)

  #Find the contour with maximum area and store it as best_cnt
  max_area = 0
  best_cnt = 1
  for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > max_area:
      max_area = area
      best_cnt = cnt

  # Find the centroid of the best_cnt and draw a circle there
  # Modify this code so that you can find the position relative to the center (Left - Negative, Right - Positive)
  M = cv2.moments(best_cnt)
  cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
  
  # Coodinate for storing the relative distance of the circle from the center (Left = Negative, Right = Positive)
  distance = -1
  # print("text:" + str(text))
  if cx != 0 and cy != 0:
      # print(cx, cy)
      distance = (cx-320, 240-cy)
      text[0] = text[0] + " " * 32 + "Distance: (" + str(distance[0]) + ", " + str(distance[1]) + ")"
  # Consider making function to fetch this value (in case the value is changed in the future)
  # Camera resolution: (640, 480) => Center should be (320, 240)
  # X increases from left to right and Y increases from bottom to
  
  # Draws a circle in the center of the scren (testing)
  cv2.circle(raw_image,(320,240),8,(0,0,0),-1)
  
        
  if max_area>0:
    cv2.circle(raw_image,(cx,cy),8,(setBounds(values[:], threshold)),-1)
    cv2.circle(raw_image,(cx,cy),4,(setBounds(values[:], threshold)),-1)
    # Draws two circles that mark the x and y coordinate respectively
    cv2.circle(raw_image, (cx,240),8,(255,0,0),-1)
    cv2.circle(raw_image, (320,cy),8,(0,0,255),-1)

  return(images,text)
#End