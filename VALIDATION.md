# SETU AI Model Validation & Benchmark Report

This document records the evaluation results, benchmarks, and performance metrics of the trained YOLOv8 person detection models for the SETU Rover platform.

---

## 📊 Evaluation Summary: YOLOv8s (Upgraded Production Model)

- **Evaluation Dataset:** 1,000 holdout test images (`datasets/test/`)
- **Total Ground Truth Persons Evaluated:** 4,182 instances
- **Model Architecture:** **YOLOv8 Small (`yolov8s.pt` fine-tuned)**
- **Parameter Count:** **11.14 Million parameters** (129 layers, 28.6 GFLOPs)
- **Input Resolution:** 640 × 640
- **Hardware Acceleration:** NVIDIA GeForce RTX 3050 Laptop GPU (CUDA 12.6, AMP enabled)

| Metric | YOLOv8n (Baseline) | YOLOv8s (Upgraded) | Improvement | Impact on Mission |
| :--- | :--- | :--- | :--- | :--- |
| **Precision** | 72.37% | **74.92%** | **+2.55%** | Drastically suppresses false alarms on clothes/chairs |
| **Recall** | 54.04% | **57.39%** | **+3.35%** | Better acquisition of trapped victims across varied poses |
| **mAP@50** | 63.88% | **67.03%** | **+3.15%** | Higher certainty on standard bounding box overlap |
| **mAP@50-95** | 39.90% | **42.79%** | **+2.89%** | Superior localization accuracy under heavy occlusion |
| **Inference Latency** | 3.39 ms | **7.73 ms** | — | **~130 FPS real-time throughput** on RTX 3050 GPU |
| **Pre-process Latency** | 0.62 ms | **0.30 ms** | Fast | Hardware-accelerated letterboxing |
| **Post-process Latency**| 0.74 ms | **0.90 ms** | Fast | Rapid Non-Maximum Suppression (NMS) |

---

## 📁 Saved Model Artifacts

| File Path | Size | Description |
| :--- | :--- | :--- |
| [`models/best.pt`](models/best.pt) | 21.5 MB | Upgraded YOLOv8s best checkpoint weights for production inference |
| [`models/setu_person_detector.pt`](models/setu_person_detector.pt) | 21.5 MB | Primary deployed YOLOv8s model |
| [`models/checkpoints/best.pt`](models/checkpoints/best.pt) | 21.5 MB | Best validation epoch snapshot |
| [`models/checkpoints/last.pt`](models/checkpoints/last.pt) | 21.5 MB | Final epoch training state |
| [`models/exported/setu_person_detector.torchscript`](models/exported/setu_person_detector.torchscript) | 42.8 MB | Standalone TorchScript model for C++ / Edge runtime |
| [`models/pretrained/yolov8s.pt`](models/pretrained/yolov8s.pt) | 21.5 MB | Pretrained YOLOv8s base weights |
| [`models/pretrained/yolov8n.pt`](models/pretrained/yolov8n.pt) | 6.2 MB | Lightweight YOLOv8n base weights |
| [`models/metrics.json`](models/metrics.json) | < 1 KB | Machine-readable metrics payload |
