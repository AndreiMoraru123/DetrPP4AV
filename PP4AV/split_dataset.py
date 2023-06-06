import os
import shutil
import numpy as np

original_dataset_dir = r"D:\PP4AV\images"
train_dir = r"D:\PP4AV\images\train"
val_dir = r"D:\PP4AV\images\val"

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

for root, dirs, files in os.walk(original_dataset_dir):
    if root not in [train_dir, val_dir]:
        np.random.shuffle(files)

        train_images = files[:int(len(files) * 0.9)]
        val_images = files[int(len(files) * 0.9):]

        for image in train_images:
            if image.endswith(('.png', '.jpg', '.jpeg')):
                shutil.copy(os.path.join(root, image), os.path.join(train_dir, image))

        for image in val_images:
            if image.endswith(('.png', '.jpg', '.jpeg')):
                shutil.copy(os.path.join(root, image), os.path.join(val_dir, image))