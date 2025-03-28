#!/usr/bin/env python3
import os
import shutil
import zipfile
import sys

def restore_raw_directory():
    # Change to the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Changed working directory to: {script_dir}")
    
    # Create raw directory if it doesn't exist
    if not os.path.exists('raw'):
        os.makedirs('raw')
    
    # Process each item in processed directory
    for item in os.listdir('processed'):
        processed_path = os.path.join('processed', item)
        
        # If it's a zipped directory or JSON
        if item.endswith('.zip'):
            # Get original name by removing .zip extension
            original_name = item[:-4]
            
            # Check if it was originally a JSON file
            if original_name.endswith('.json'):
                # Extract the JSON file to raw directory
                with zipfile.ZipFile(processed_path, 'r') as zipf:
                    zipf.extract(original_name, 'raw')
                print(f"Restored JSON file: {original_name}")
            else:
                # Extract the directory to raw
                extract_path = os.path.join('raw', original_name)
                os.makedirs(extract_path, exist_ok=True)
                
                with zipfile.ZipFile(processed_path, 'r') as zipf:
                    # Extract all contents
                    for zip_info in zipf.infolist():
                        if '/' in zip_info.filename:
                            # Has directory structure
                            directory = os.path.dirname(zip_info.filename)
                            if not os.path.exists(os.path.join('raw', directory)):
                                os.makedirs(os.path.join('raw', directory))
                        zipf.extract(zip_info, 'raw')
                
                print(f"Restored directory: {original_name}")
        
        # Otherwise, just copy it (not move from processed)
        else:
            shutil.copy2(processed_path, os.path.join('raw', item))
            print(f"Restored file: {item}")

if __name__ == "__main__":
    restore_raw_directory()
    print("Restoration complete!")