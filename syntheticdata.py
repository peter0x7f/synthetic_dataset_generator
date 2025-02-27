import os
import random
from PIL import Image

def overlay_png_on_images(base_folder, overlay_path, output_folder, baseimgx,baseimgy, scalemin,scalemax):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    base_width, base_height = baseimgx, baseimgy  # Base image dimensions
    overlay_img = Image.open(overlay_path).convert("RGBA")
    
    for filename in os.listdir(base_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            base_img_path = os.path.join(base_folder, filename)
            base_img = Image.open(base_img_path).convert("RGBA")
            
            for i in range(5):  
                new_img = base_img.copy()
                
                # Determine random scale % of base image size, use 0.01
                scale_factor = random.uniform(scalemin, scalemax)
                new_width = int(base_width * scale_factor)
                new_height = int(overlay_img.height * (new_width / overlay_img.width))
                resized_overlay = overlay_img.resize((new_width, new_height), Image.ANTIALIAS)
                
                # Determine random position within bounds
                max_x = base_width - new_width
                max_y = base_height - new_height
                x_offset = random.randint(0, max_x)
                y_offset = random.randint(0, max_y)
                
                # Overlay PNG onto image
                new_img.paste(resized_overlay, (x_offset, y_offset), resized_overlay)
                
                # Save modified image
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_overlay_{i}.png")
                new_img.save(output_path, "PNG")
                print(f"Saved: {output_path}")


base_folder = r"putpathtobaseimagefolder(I used https://www.kaggle.com/datasets/vinayakshanawad/weedcrop-image-dataset?resource=download and https://zenodo.org/records/7951745"
overlay_path = r"png you want to place over"
output_folder = r"synth_dataset"
overlay_png_on_images(base_folder2, overlay_path, output_folder, 1280, 720, 0.07, 0.25) #change values based on your datatsets. 
