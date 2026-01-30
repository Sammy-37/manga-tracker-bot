import os
import cv2
import shutil
from ultralytics import YOLO

# 1. LOAD THE AI MODEL

model = YOLO("manga_yolo.pt")

def extract_folder(folder_path):
    print(f"AI Scanning folder: {folder_path}...")
    
    # Get all images
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    for img_file in image_files:
        full_path = os.path.join(folder_path, img_file)
        
        # 2. RUN INFERENCE (The Magic Step)
        # conf=0.5 means "Only keep boxes you are 50% sure about"
        results = model.predict(full_path, conf=0.5, verbose=False)
        
        # results is a list (one per image). We only sent one.
        result = results[0]
        
        # 3. PROCESS RESULTS
        # The AI returns boxes in format: [x, y, x2, y2]
        boxes = result.boxes.xyxy.cpu().numpy()
        
        if len(boxes) == 0:
            print(f"No panels found in {img_file}")
            continue

        # Sort panels top-to-bottom so they are in reading order
        # (We sort by the Y-coordinate of the top-left corner)
        boxes = sorted(boxes, key=lambda b: b[1])
        
        # Load the original image to crop it
        original_img = cv2.imread(full_path)
        
        print(f"Found {len(boxes)} panels in {img_file}")
        
        # 4. CROP AND SAVE
        base_name = os.path.splitext(img_file)[0]
        
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box) # Convert decimals to integers
            
            # Crop: image[y:y2, x:x2]
            crop = original_img[y1:y2, x1:x2]
            
            # Save
            output_filename = f"panels/{base_name}_p{i}.jpg"
            cv2.imwrite(output_filename, crop)
            print(f"   Saved {output_filename}")

# Run it
if not os.path.exists("panels"):
    os.makedirs("panels")

extract_folder("raw_pages")
