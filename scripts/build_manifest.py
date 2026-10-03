import csv
from pathlib import Path

RAW_DIR = Path('../datasets/raw/coco_person')
MANIFEST_DIR = Path('../datasets/manifests')
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

rows = []

def scan(split_folder, split_hint):
    img_dir = RAW_DIR / split_folder / 'images'
    lbl_dir = RAW_DIR / split_folder / 'labels'
    if not img_dir.exists():
        print(f'WARNING: missing {img_dir}')
        return
    for img_path in sorted(img_dir.glob('*.*')):
        stem = img_path.stem
        lbl_path = lbl_dir / f'{stem}.txt'
        rows.append({
            'filename': img_path.name,
            'image_path': str(img_path.as_posix()),
            'label_path': str(lbl_path.as_posix()) if lbl_path.exists() else '',
            'source': 'coco_person',
            'session_id': stem,
            'split_hint': split_hint,
        })

scan('train', 'train_pool')
scan('val', 'test_pool')

out_path = MANIFEST_DIR / 'manifest.csv'
with open(out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['filename', 'image_path', 'label_path', 'source', 'session_id', 'split_hint'])
    writer.writeheader()
    writer.writerows(rows)

print(f'Wrote {len(rows)} rows to {out_path}')
print(f'Images missing label files: {sum(1 for r in rows if r["label_path"] == "")}')
