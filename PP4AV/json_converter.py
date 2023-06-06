import os
import json
from PIL import Image


def get_image_list(image_dir):
    return os.listdir(image_dir)


def convert_annotations(annotation_dir, train_image_dir, val_image_dir, train_images, val_images):
    train_annotations = {
        "images": [],
        "annotations": [],
        "categories": [
            {"id": 0, "name": "face"},
            {"id": 1, "name": "license plate"}
        ]
    }

    val_annotations = {
        "images": [],
        "annotations": [],
        "categories": [
            {"id": 0, "name": "face"},
            {"id": 1, "name": "license plate"}
        ]
    }

    image_id = 0
    annotation_id = 0

    folders = [
        folder for folder in os.listdir(annotation_dir)
        if os.path.isdir(os.path.join(annotation_dir, folder))
    ]

    for folder in folders:
        folder_path = os.path.join(annotation_dir, folder)
        annotation_files = [
            file_name for file_name in os.listdir(folder_path)
            if file_name.endswith(".txt") and not file_name.endswith(".zip")
        ]

        for file_name in annotation_files:
            annotation_file = os.path.join(folder_path, file_name)
            image_name = file_name.replace(".txt", ".png")

            if image_name in train_images:
                target_annotations = train_annotations
                image_path = os.path.join(train_image_dir, image_name)
            elif image_name in val_images:
                target_annotations = val_annotations
                image_path = os.path.join(val_image_dir, image_name)
            else:
                continue

            width, height = get_image_dimensions(image_path)

            image_info = {
                "id": image_id,
                "file_name": image_name,
                "width": width,
                "height": height
            }
            target_annotations["images"].append(image_info)

            with open(annotation_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split()
                    cls = int(line[0])
                    x_center = float(line[1])
                    y_center = float(line[2])
                    bbox_width = float(line[3])
                    bbox_height = float(line[4])

                    x_min = (x_center - bbox_width / 2) * width
                    y_min = (y_center - bbox_height / 2) * height
                    bbox_width *= width
                    bbox_height *= height

                    annotation = {
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": cls,
                        "bbox": [x_min, y_min, bbox_width, bbox_height],
                        "area": bbox_width * bbox_height,
                        "iscrowd": 0
                    }
                    target_annotations["annotations"].append(annotation)

                    annotation_id += 1

            image_id += 1

    return train_annotations, val_annotations


def get_image_dimensions(image_path):
    image = Image.open(image_path)
    width, height = image.size
    return width, height


train_image_dir = r"D:\PP4AV\images\train"
val_image_dir = r"D:\PP4AV\images\val"
annotation_dir = r"D:\PP4AV\annotations"

train_images = get_image_list(train_image_dir)
val_images = get_image_list(val_image_dir)

train_annotations, val_annotations = convert_annotations(annotation_dir, train_image_dir, val_image_dir, train_images,
                                                         val_images)

with open(os.path.join(train_image_dir, "coco_format_train.json"), "w") as f:
    json.dump(train_annotations, f)

with open(os.path.join(val_image_dir, "coco_format_val.json"), "w") as f:
    json.dump(val_annotations, f)
