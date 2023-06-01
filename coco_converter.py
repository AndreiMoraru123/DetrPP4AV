import os
import json
import xml.etree.ElementTree as ET


def get_label_info(label_path):
    tree = ET.parse(label_path)
    root = tree.getroot()

    file_name = root.find("filename").text
    img_size = root.find("size")
    width = int(img_size.find("width").text)
    height = int(img_size.find("height").text)

    annotations = []
    for obj in root.findall("object"):
        name = obj.find("name").text
        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        annotation = {
            "category_id": 1,  # assuming there's only one category
            "bbox": [xmin, ymin, xmax - xmin, ymax - ymin],
            "area": (xmax - xmin) * (ymax - ymin),
            "iscrowd": 0
        }
        annotations.append(annotation)

    image_info = {
        "file_name": file_name,
        "height": height,
        "width": width
    }

    return image_info, annotations


def convert_to_coco_format(label_dir, img_dir):
    images = []
    annotations = []

    for idx, label_file in enumerate(os.listdir(label_dir)):
        label_path = os.path.join(label_dir, label_file)
        # Ensure that the corresponding image file exists in img_dir
        if not os.path.exists(os.path.join(img_dir, os.path.splitext(label_file)[0] + ".png")):
            continue

        image_info, annos = get_label_info(label_path)
        image_info["id"] = idx
        # Include only the filename, not the path
        image_info["file_name"] = os.path.splitext(label_file)[0] + ".png"
        images.append(image_info)

        for anno in annos:
            anno["image_id"] = idx
            anno["id"] = len(annotations) + 1
            annotations.append(anno)

    coco_format_json = {
        "images": images,
        "annotations": annotations,
        "categories": [
            {"id": 1, "name": "licence"}
        ]
    }

    # Write to separate JSON files for train and val
    with open(os.path.join(img_dir, f"coco_format_{os.path.basename(img_dir)}.json"), "w") as f:
        json.dump(coco_format_json, f)


if __name__ == "__main__":
    annotations_dir = r"D:\LicensePlates\annotations"
    train_img_dir = r"D:\LicensePlates\images\train"
    val_img_dir = r"D:\LicensePlates\images\val"

    convert_to_coco_format(annotations_dir, train_img_dir)
    convert_to_coco_format(annotations_dir, val_img_dir)




