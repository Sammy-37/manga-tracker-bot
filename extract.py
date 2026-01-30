import os
import subprocess
import shutil

output_dir = "panels"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def extract_panels(image_path):
    print(f"Processing {image_path}...")
    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    expected_output_folder = base_name 

    command = [
        "python", "pst.py",
        "--filepath", image_path,
        "--nosaveimage" 
    ]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error processing image: {e}")
        return

    if os.path.exists(expected_output_folder):
        files = sorted(os.listdir(expected_output_folder))
        
        for i, f in enumerate(files):
            src = os.path.join(expected_output_folder, f)
            
            new_name = f"panel_{i}.jpg"
            dst = os.path.join(output_dir, new_name)
            
            shutil.move(src, dst)
            print(f"Saved {dst}")
        
        os.rmdir(expected_output_folder)
    else:
        print("No panels found or tool failed.")

extract_panels("raw_pages/test.jpg")
