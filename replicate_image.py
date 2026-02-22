import os
import shutil

input_folder = "images"      
output_folder = "output_images"    

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Get list of images
images = [f for f in os.listdir(input_folder) 
          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

counter = 1

for i in range(15):  
    for img in images:
        src_path = os.path.join(input_folder, img)

        # Keep same extension
        ext = os.path.splitext(img)[1]

        new_name = f"image_{counter}{ext}"
        dst_path = os.path.join(output_folder, new_name)

        shutil.copy(src_path, dst_path)

        counter += 1

print("Done! Images duplicated 15x successfully.")
