import cv2
import os
import numpy as np
if not os.path.exists("panels"):
    os.makedirs("panels")

def extract_panels(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not read image.")
        return
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((5,5),np.uint8)

    dilate = cv2.dilate(thresh,kernel,iterations=1)
    contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    height,width=img.shape[:2]
    total_area=width*height
    min_area=total_area*0.03

    panel_count = 0

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        
        current_area = w*h
        aspect_ratio=w/h

        if current_area < min_area:
            continue
        if aspect_ratio > 5 or aspect_ratio <0.2:
            continue

        crop = img[y:y+h, x:x+w]

        filename = f"panels/panel_{panel_count}.jpg"
        cv2.imwrite(filename, crop)
        print(f"Saved {filename}")
        panel_count += 1

extract_panels("raw_pages/test.jpg")
