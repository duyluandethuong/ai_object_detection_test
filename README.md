# Image/Video Object Detection Project

This project uses YOLOv8 for object detection in images and videos. It supports both single image, batch processing of multiple images, and video processing. The project utilizes GPU acceleration for faster processing and selects the highest confidence detection for each object type.

## Features
- Single image or batch folder processing
- Video file processing
- GPU acceleration support (NVIDIA CUDA and Apple MPS)
- Multiple YOLOv8 model options
- Highest confidence detection selection
- Object detection with bounding boxes and labels
- Automatic timestamp-based output folder creation
- Processing time logging
- Real-time video processing progress

## Requirements
- Python 3.8+
- CUDA-compatible GPU (for NVIDIA GPUs)
- MPS support (for Mac with M1/M2 chips)
- Virtual environment

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. For single image processing:
```bash
python detect.py --image path/to/your/image.jpg
```

2. For batch processing of a folder:
```bash
python detect.py --folder path/to/your/folder
```

3. For video processing:
```bash
python detect.py --video path/to/your/video.mp4
```

### Available Models
You can choose from the following YOLOv8 models:
- `yolov8n.pt` (nano) - Fastest, smallest model
- `yolov8s.pt` (small) - Good balance of speed and accuracy
- `yolov8m.pt` (medium) - Better accuracy, moderate speed (default)
- `yolov8l.pt` (large) - High accuracy, slower speed
- `yolov8x.pt` (extra large) - Best accuracy, slowest speed

Example with different model:
```bash
python detect.py --video input.mp4 --model yolov8l.pt
```

## Output
- Processed images/videos with bounding boxes and labels are saved in timestamped subfolders within the `output` directory
- Each run creates a new subfolder named `run_YYYYMMDD_HHMMSS`
- Processing time is logged in the console
- For videos, progress is shown every 100 frames
- Only the highest confidence detection is shown for each object type

## Notes
- The script automatically uses GPU acceleration if available
- Supported image formats: JPG, JPEG, PNG
- Supported video formats: MP4, AVI, MOV
- Output includes confidence scores for each detected object
- Larger models provide better accuracy but require more processing time and GPU memory
- Video processing shows real-time progress and average FPS
- Only the highest confidence detection is shown for each object type to reduce clutter
- The default model (yolov8m.pt) provides a good balance between accuracy and speed 