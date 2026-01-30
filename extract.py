import os
import subprocess
import shutil

output_dir = "panels"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def extract_folder(folder_path):
    print(f"Processing folder: {folder_path}...")
    
    # 1. Run the tool on the entire FOLDER
    command = ["python", "pst.py", "--filepath", folder_path, "--nosaveimage"]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return

    # 2. Loop through all images in the input folder to find their outputs
    # (pst.py creates a folder named after each image file)
    if os.path.exists(folder_path):
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png'))]
    
    for img_file in image_files:
        base_name = os.path.splitext(img_file)[0] # e.g. "test"
        tool_output_folder = base_name 
        
        # If the tool successfully created a folder for this image...
        if os.path.exists(tool_output_folder):
            files = sorted(os.listdir(tool_output_folder))
            
            # Move and rename the panels
            for i, f in enumerate(files):
                src = os.path.join(tool_output_folder, f)
                new_name = f"{base_name}_p{i}.jpg" # e.g. "test_p0.jpg"
                dst = os.path.join("panels", new_name)
                shutil.move(src, dst)
            
            # Clean up the empty temp folder
            os.rmdir(tool_output_folder)
            print(f"✅ Extracted {len(files)} panels from {img_file}")

extract_folder("raw_pages/")
