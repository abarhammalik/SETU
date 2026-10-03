import os
import shutil
from pathlib import Path
import fiftyone as fo
import fiftyone.zoo as foz

def add_negative_samples():
    print("Loading COCO validation samples that DO NOT contain persons...")
    # Load dataset from local cache
    ds = foz.load_zoo_dataset(
        "coco-2017",
        split="validation",
        label_types=["detections"],
        dataset_name="coco_bg_fetch"
    )

    # Filter samples that DO NOT contain any 'person' detection
    # This gives pure negative background images: rooms, furniture, chairs, tables, etc.
    bg_view = ds.filter_labels("ground_truth", ~fo.ViewField("label").is_in(["person"]))

    train_img_dir = Path("datasets/train/images")
    train_lbl_dir = Path("datasets/train/labels")
    val_img_dir = Path("datasets/val/images")
    val_lbl_dir = Path("datasets/val/labels")

    train_count = 0
    val_count = 0

    print("Copying negative background images to training set...")
    for idx, sample in enumerate(bg_view):
        src_path = Path(sample.filepath)
        if not src_path.exists():
            continue

        # Check that this sample truly has no person
        labels = [d.label for d in (sample.ground_truth.detections if sample.ground_truth else [])]
        if "person" in labels:
            continue

        if train_count < 250:
            dst_img = train_img_dir / f"bg_{src_path.name}"
            dst_lbl = train_lbl_dir / f"bg_{src_path.stem}.txt"
            shutil.copy2(src_path, dst_img)
            dst_lbl.touch() # Empty label file = negative background sample for YOLO
            train_count += 1
        elif val_count < 50:
            dst_img = val_img_dir / f"bg_{src_path.name}"
            dst_lbl = val_lbl_dir / f"bg_{src_path.stem}.txt"
            shutil.copy2(src_path, dst_img)
            dst_lbl.touch()
            val_count += 1
        else:
            break

    print(f"Added {train_count} negative background images to train set.")
    print(f"Added {val_count} negative background images to val set.")

if __name__ == "__main__":
    add_negative_samples()
