import os
import random
from PIL import Image

def overlay_png_on_images(base_folder, overlay_path, output_folder, baseimgx, baseimgy, scalemin, scalemax, class_id):
    # Create folders for images and annotations if they don't exist
    images_folder = os.path.join(output_folder, "images")
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    annotations_folder = os.path.join(output_folder, "labels")
    if not os.path.exists(annotations_folder):
        os.makedirs(annotations_folder)
    
    base_width, base_height = baseimgx, baseimgy  # Base image dimensions
    overlay_img = Image.open(overlay_path).convert("RGBA")
    
    for filename in os.listdir(base_folder)[:100]:
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            base_img_path = os.path.join(base_folder, filename)
            base_img = Image.open(base_img_path).convert("RGBA")
            
            for i in range(5):  
                new_img = base_img.copy()
                
                # Determine random scale % of base image size, use 0.01
                scale_factor = random.uniform(scalemin, scalemax)
                new_width = int(base_width * scale_factor)
                new_height = int(overlay_img.height * (new_width / overlay_img.width))
                resized_overlay = overlay_img.resize((new_width, new_height))
                
                # Determine random position within bounds
                max_x = base_width - new_width
                max_y = base_height - new_height
                x_offset = random.randint(0, max_x)
                y_offset = random.randint(0, max_y)
                
                # Overlay PNG onto image
                new_img.paste(resized_overlay, (x_offset, y_offset), resized_overlay)
                
                # Save modified image
                image_output_path = os.path.join(images_folder, f"{os.path.splitext(filename)[0]}_overlay_{i}.png")
                with open(image_output_path, "wb") as f:
                    new_img.save(f, "PNG")

                # Calculate YOLO format annotations (normalized)
                x_center = (x_offset + new_width / 2) / base_width
                y_center = (y_offset + new_height / 2) / base_height
                width_norm = new_width / base_width
                height_norm = new_height / base_height

                # Save annotation file
                annotation_filename = f"{os.path.splitext(filename)[0]}_overlay_{i}.txt"
                output_annotation_path = os.path.join(annotations_folder, annotation_filename)
                with open(output_annotation_path, "w") as f:
                    f.write(f"{class_id} {x_center} {y_center} {width_norm} {height_norm}")
                    # class_id is 0 by default, we may need to rework this part - PS


base_folder = r"original_images"  # Folder where original images are located
overlay_path = r"pfm1-landmine-image01.png"  # Image that you'd like to overlay
output_folder = r"synth_dataset"  # Folder where new images should be placed
# Change values based on your datasets
overlay_png_on_images(base_folder, overlay_path, output_folder, 1280, 720, 0.07, 0.25, 0)

# Images sourced from https://www.kaggle.com/datasets/vinayakshanawad/weedcrop-image-dataset
# and from https://zenodo.org/records/7951745