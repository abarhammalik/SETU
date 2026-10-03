import argparse
import time
from pathlib import Path
import cv2
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="SETU Rover - Live Edge AI Person Detection")
    parser.add_argument("--model", type=str, default="models/best.pt", help="Path to trained model weights")
    parser.add_argument("--source", type=str, default="0", help="Camera index (e.g. 0), video file path, or image path")
    parser.add_argument("--conf", type=float, default=0.55, help="Confidence threshold (0.0 to 1.0, default 0.55 to reject false positives)")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference resolution")
    parser.add_argument("--save", action="store_true", help="Save annotated output video/images")
    parser.add_argument("--save-dir", type=str, default="runs/detect", help="Output directory when saving")
    return parser.parse_args()

def main():
    args = parse_args()
    model_path = Path(args.model)
    if not model_path.exists():
        print(f"[ERROR] Model file not found at: {model_path}")
        print("Please ensure the model is trained and saved in 'models/best.pt'.")
        return

    print(f"[*] Loading SETU AI Detector from {model_path}...")
    model = YOLO(str(model_path))

    source = int(args.source) if args.source.isdigit() else args.source
    print(f"[*] Connecting to source: {source} (Confidence threshold: {args.conf})...")
    print("[*] Press 'q' or 'ESC' in the display window to exit.")

    window_title = "SETU Rover - Real-Time Person Detection"
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)

    prev_time = time.time()

    # Stream predictions
    results = model.predict(
        source=source,
        conf=args.conf,
        imgsz=args.imgsz,
        save=args.save,
        project=args.save_dir,
        name="predict",
        exist_ok=True,
        stream=True,
        verbose=False
    )

    for r in results:
        curr_time = time.time()
        fps = 1.0 / max((curr_time - prev_time), 1e-5)
        prev_time = curr_time

        # Plot ultralytics bounding boxes and labels
        frame = r.plot()

        boxes = r.boxes
        num_persons = len(boxes) if boxes is not None else 0

        # Draw search & rescue HUD overlay
        h, w = frame.shape[:2]

        # Top banner bar
        banner_h = 60
        overlay = frame.copy()
        
        if num_persons > 0:
            top_conf = max([float(c) for c in boxes.conf]) * 100.0
            banner_color = (0, 0, 180) # Red alert
            status_text = f"ALERT: {num_persons} PERSON DETECTED  |  MAX CONF: {top_conf:.1f}%"
        else:
            banner_color = (40, 40, 40) # Dark neutral
            status_text = "STATUS: SEARCHING / PATROLLING (NO PERSON DETECTED)"

        cv2.rectangle(overlay, (0, 0), (w, banner_h), banner_color, -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        # Status & FPS text
        cv2.putText(frame, status_text, (20, 38), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
        fps_text = f"FPS: {fps:.1f} | Conf Thr: {int(args.conf * 100)}%"
        cv2.putText(frame, fps_text, (w - 280, 38), cv2.FONT_HERSHEY_DUPLEX, 0.55, (200, 255, 200), 1, cv2.LINE_AA)

        # Bottom help bar
        cv2.putText(frame, "Press 'q' or 'ESC' to exit", (20, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1, cv2.LINE_AA)

        # Show frame on screen
        cv2.imshow(window_title, frame)

        # Check for exit key
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            print("[*] Exit requested by user.")
            break

    cv2.destroyAllWindows()
    print("[*] Stream closed successfully.")

if __name__ == "__main__":
    main()
