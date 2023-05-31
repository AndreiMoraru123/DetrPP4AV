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


def convert_to_coco_format(label_dir):
    images = []
    annotations = []

    for idx, label_file in enumerate(os.listdir(label_dir)):
        label_path = os.path.join(label_dir, label_file)

        image_info, annos = get_label_info(label_path)
        image_info["id"] = idx
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

    with open("coco_format.json", "w") as f:
        json.dump(coco_format_json, f)


if __name__ == "__main__":
    convert_to_coco_format(r"D:\LicensePlates\annotations")
