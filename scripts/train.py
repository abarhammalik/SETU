import argparse
import json
import shutil
import sys
from pathlib import Path
import torch
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="Train YOLO person detection model for SETU Rover")
    parser.add_argument("--data", type=str, default="datasets/data.yaml", help="Path to data.yaml")
    parser.add_argument("--weights", type=str, default="models/pretrained/yolov8n.pt", help="Pretrained weights")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=8, help="Batch size (default 8)")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--device", type=str, default="0" if torch.cuda.is_available() else "cpu", help="CUDA device or cpu")
    parser.add_argument("--workers", type=int, default=0, help="Number of dataloader workers (0 for Windows stability)")
    parser.add_argument("--project", type=str, default="runs/train", help="Training project folder")
    parser.add_argument("--name", type=str, default="setu_person_detector", help="Experiment name")
    return parser.parse_args()

def main():
    args = parse_args()
    workspace_root = Path(__file__).resolve().parent.parent
    data_path = (workspace_root / args.data).resolve()
    weights_path = (workspace_root / args.weights).resolve()
    models_dir = workspace_root / "models"
    checkpoints_dir = models_dir / "checkpoints"
    exported_dir = models_dir / "exported"

    models_dir.mkdir(parents=True, exist_ok=True)
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    exported_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("SETU Rover - Edge AI Model Training")
    print("=" * 60)
    print(f"Data config   : {data_path}")
    print(f"Base weights  : {weights_path}")
    print(f"Epochs        : {args.epochs}")
    print(f"Batch size    : {args.batch}")
    print(f"Image size    : {args.imgsz}")
    print(f"Device        : {args.device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
    print(f"Workers       : {args.workers}")
    print("=" * 60)

    # Initialize model
    model = YOLO(str(weights_path))

    # Train model
    print("\n[1/4] Starting model training...")
    train_results = model.train(
        data=str(data_path),
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        workers=args.workers,
        project=str(workspace_root / args.project),
        name=args.name,
        exist_ok=True,
        save=True,
        plots=True,
        verbose=True
    )

    train_save_dir = Path(train_results.save_dir) if hasattr(train_results, 'save_dir') else workspace_root / args.project / args.name
    best_weights_src = train_save_dir / "weights" / "best.pt"
    last_weights_src = train_save_dir / "weights" / "last.pt"

    print("\n[2/4] Saving model artifacts to 'models' folder...")
    models_dir.mkdir(parents=True, exist_ok=True)
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    exported_dir.mkdir(parents=True, exist_ok=True)
    if best_weights_src.exists():
        shutil.copy2(best_weights_src, models_dir / "best.pt")
        shutil.copy2(best_weights_src, models_dir / "setu_person_detector.pt")
        shutil.copy2(best_weights_src, checkpoints_dir / "best.pt")
        print(f"  -> Saved best weights to {models_dir / 'best.pt'}")
        print(f"  -> Saved best weights to {models_dir / 'setu_person_detector.pt'}")
        print(f"  -> Saved checkpoint to {checkpoints_dir / 'best.pt'}")
    else:
        print(f"  WARNING: Best weights not found at {best_weights_src}")

    if last_weights_src.exists():
        shutil.copy2(last_weights_src, checkpoints_dir / "last.pt")
        print(f"  -> Saved checkpoint to {checkpoints_dir / 'last.pt'}")

    # Evaluate on test set
    print("\n[3/4] Evaluating best model on test set...")
    best_model = YOLO(str(models_dir / "best.pt"))
    val_results = best_model.val(
        data=str(data_path),
        split="test",
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        workers=args.workers
    )

    metrics = {
        "mAP50": float(val_results.box.map50) if hasattr(val_results.box, 'map50') else None,
        "mAP50_95": float(val_results.box.map) if hasattr(val_results.box, 'map') else None,
        "precision": float(val_results.box.mp) if hasattr(val_results.box, 'mp') else None,
        "recall": float(val_results.box.mr) if hasattr(val_results.box, 'mr') else None,
        "speed_preprocess_ms": float(val_results.speed.get("preprocess", 0)),
        "speed_inference_ms": float(val_results.speed.get("inference", 0)),
        "speed_postprocess_ms": float(val_results.speed.get("postprocess", 0)),
        "epochs_trained": args.epochs,
        "classes": ["person"]
    }

    metrics_file = models_dir / "metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
    print(f"  -> Saved validation metrics to {metrics_file}")
    print(f"  mAP@50     : {metrics['mAP50']:.4f}")
    print(f"  mAP@50:95  : {metrics['mAP50_95']:.4f}")
    print(f"  Precision  : {metrics['precision']:.4f}")
    print(f"  Recall     : {metrics['recall']:.4f}")
    print(f"  Inference  : {metrics['speed_inference_ms']:.2f} ms/frame")

    # Export model for edge deployment
    print("\n[4/4] Exporting model to TorchScript for edge deployment...")
    try:
        exported_path = best_model.export(format="torchscript", imgsz=args.imgsz)
        exported_path = Path(exported_path)
        target_exported = exported_dir / "setu_person_detector.torchscript"
        shutil.copy2(exported_path, target_exported)
        print(f"  -> Exported edge model to {target_exported}")
    except Exception as e:
        print(f"  Export failed: {e}")

    print("\n" + "=" * 60)
    print("Training and model saving completed successfully!")
    print(f"Models directory: {models_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
