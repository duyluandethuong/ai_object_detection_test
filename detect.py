import argparse
import time
from pathlib import Path
from ultralytics import YOLO
import utils
import torch
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description="Image/Video Object Detection using YOLOv8")
    parser.add_argument("--image", type=str, help="Path to a single image")
    parser.add_argument("--folder", type=str, help="Path to a folder containing images")
    parser.add_argument("--video", type=str, help="Path to a video file")
    parser.add_argument("--model", type=str, default="yolov8m.pt", 
                       choices=["yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt"],
                       help="YOLOv8 model to use (default: yolov8m.pt)")
    args = parser.parse_args()

    # Get the best available device
    device = utils.get_device()
    utils.print_device_info(device)

    # Load selected YOLOv8 model
    print(f"Loading model: {args.model}")
    model = YOLO(args.model)
    model.to(device)

    # Create output directory
    output_dir = utils.create_output_dir()
    print(f"Output will be saved to: {output_dir}")

    # Start timing
    start_time = time.time()

    if args.image:
        # Process single image
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"Error: Image not found at {args.image}")
            return
        utils.process_image(model, image_path, output_dir)

    elif args.folder:
        # Process folder of images
        folder_path = Path(args.folder)
        if not folder_path.exists():
            print(f"Error: Folder not found at {args.folder}")
            return

        # Get all image files
        image_files = utils.get_image_files(folder_path)

        if not image_files:
            print(f"No images found in {args.folder}")
            return

        print(f"\nProcessing {len(image_files)} images...")
        for image_path in tqdm(image_files, desc="Processing images"):
            utils.process_image(model, image_path, output_dir)

    elif args.video:
        # Process video file
        video_path = Path(args.video)
        if not video_path.exists():
            print(f"Error: Video not found at {args.video}")
            return
        utils.process_video(model, video_path, output_dir, progress_bar=True)

    else:
        print("Please provide either --image, --folder, or --video argument")
        return

    # Calculate and print total processing time
    end_time = time.time()
    total_processing_time = end_time - start_time
    
    # Get device details for final log
    device_details = "CPU"
    if device == "cuda":
        device_details = f"CUDA ({torch.cuda.get_device_name(0)})"
    elif device == "mps":
        device_details = "MPS (Metal Performance Shaders)"
    
    print(f"\nProcessing Summary:")
    print(f"  - Total processing time: {total_processing_time:.2f} seconds")
    print(f"  - Device used: {device_details}")
    print(f"  - Model: {args.model}")
    print(f"  - Output directory: {output_dir}")

if __name__ == "__main__":
    main() 