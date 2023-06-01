import os
import shutil
import numpy as np

original_dataset_dir = r"D:\LicensePlates\images"
train_dir = r"D:\LicensePlates\images\train"
val_dir = r"D:\LicensePlates\images\val"

all_images = os.listdir(original_dataset_dir)
np.random.shuffle(all_images)

train_images = all_images[:int(len(all_images) * 0.9)]
val_images = all_images[int(len(all_images) * 0.9):]

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

for image in train_images:
    if image.endswith(('.png', '.jpg', '.jpeg')):
        shutil.copy(os.path.join(original_dataset_dir, image), os.path.join(train_dir, image))

for image in val_images:
    if image.endswith(('.png', '.jpg', '.jpeg')):
        shutil.copy(os.path.join(original_dataset_dir, image), os.path.join(val_dir, image))

for image in all_images:
    if os.path.isfile(os.path.join(original_dataset_dir, image)) and image.endswith(('.png', '.jpg', '.jpeg')):
        original_file_path = os.path.join(original_dataset_dir, image)
        os.remove(original_file_path)








