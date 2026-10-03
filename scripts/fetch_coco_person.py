import fiftyone as fo
import fiftyone.zoo as foz
import os

os.makedirs("../datasets/raw/coco_person", exist_ok=True)

print("Downloading COCO train subset (person class, 4000 images)...")
train_ds = foz.load_zoo_dataset(
    "coco-2017",
    split="train",
    label_types=["detections"],
    classes=["person"],
    max_samples=4000,
    dataset_name="coco_person_train",
    shuffle=True,
    seed=42,
)

print("Downloading COCO validation subset (person class, 1000 images)...")
val_ds = foz.load_zoo_dataset(
    "coco-2017",
    split="validation",
    label_types=["detections"],
    classes=["person"],
    max_samples=1000,
    dataset_name="coco_person_val",
    shuffle=True,
    seed=42,
)

train_ds.export(
    export_dir="../datasets/raw/coco_person/train",
    dataset_type=fo.types.YOLOv5Dataset,
    classes=["person"],
    label_field="ground_truth",
)

val_ds.export(
    export_dir="../datasets/raw/coco_person/val",
    dataset_type=fo.types.YOLOv5Dataset,
    classes=["person"],
    label_field="ground_truth",
)

print("DONE")
print("Train samples:", len(train_ds))
print("Val samples:", len(val_ds))
