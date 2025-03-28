#!/usr/bin/env python3
import os
import shutil
import zipfile

def process_raw_directory():
    # Change to the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Changed working directory to: {script_dir}")
    
    # Create processed directory if it doesn't exist
    if not os.path.exists('processed'):
        os.makedirs('processed')
    
    # Process each item in raw directory
    for item in os.listdir('raw'):
        raw_path = os.path.join('raw', item)
        
        # If directory, zip it
        if os.path.isdir(raw_path):
            zip_path = os.path.join('processed', f"{item}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Walk through all files and directories inside the directory
                for root, dirs, files in os.walk(raw_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calculate the arcname (path inside the zip file)
                        arcname = os.path.relpath(file_path, start=os.path.dirname(raw_path))
                        zipf.write(file_path, arcname)
            print(f"Zipped directory: {item}")
        
        # If JSON file, zip it
        elif item.endswith('.json'):
            zip_path = os.path.join('processed', f"{item}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(raw_path, item)
            print(f"Zipped JSON file: {item}")
        
        # Otherwise, just copy it (not move)
        else:
            shutil.copy2(raw_path, os.path.join('processed', item))
            print(f"Copied file: {item}")

if __name__ == "__main__":
    process_raw_directory()
    print("Processing complete!")