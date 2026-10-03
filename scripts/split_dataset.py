import csv
import random
import shutil
from pathlib import Path

MANIFEST_PATH = Path('../datasets/manifests/manifest.csv')
DATASET_ROOT = Path('../datasets')
SEED = 42
VAL_HOLDOUT = 500

random.seed(SEED)

with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

train_pool = [r for r in rows if r['split_hint'] == 'train_pool']
test_pool = [r for r in rows if r['split_hint'] == 'test_pool']

session_ids = sorted(set(r['session_id'] for r in train_pool))
random.shuffle(session_ids)
val_sessions = set(session_ids[:VAL_HOLDOUT])

def assign(r):
    if r['split_hint'] == 'test_pool':
        return 'test'
    return 'val' if r['session_id'] in val_sessions else 'train'

for r in rows:
    r['final_split'] = assign(r)

def copy_files(r):
    split = r['final_split']
    img_src = Path(r['image_path'])
    lbl_src = Path(r['label_path']) if r['label_path'] else None
    img_dst_dir = DATASET_ROOT / split / 'images'
    lbl_dst_dir = DATASET_ROOT / split / 'labels'
    img_dst_dir.mkdir(parents=True, exist_ok=True)
    lbl_dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(img_src, img_dst_dir / img_src.name)
    if lbl_src and lbl_src.exists():
        shutil.copy2(lbl_src, lbl_dst_dir / lbl_src.name)

for r in rows:
    copy_files(r)

updated_path = Path('../datasets/manifests/manifest_split.csv')
with open(updated_path, 'w', newline='', encoding='utf-8') as f:
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

counts = {}
for r in rows:
    counts[r['final_split']] = counts.get(r['final_split'], 0) + 1

print('Split complete.')
print(counts)
