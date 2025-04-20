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
- Modern GUI with dark/light theme support
- Progress tracking and status updates

## Requirements
- Python 3.8+
- CUDA-compatible GPU (for NVIDIA GPUs)
- MPS support (for Mac with M1/M2 chips)
- Virtual environment
- PyTorch
- OpenCV
- Ultralytics YOLOv8
- Tkinter (usually comes with Python)

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

### Running the GUI Application

To run the graphical user interface:

```bash
python -m gui.main
```

The GUI provides the following features:

1. **Model Selection**: Choose from different YOLOv8 models (n, s, m, l, x)
2. **Input Selection**: 
   - Select a single image file
   - Select a video file
   - Select a folder containing images
3. **Preview Windows**:
   - Left window shows the original input
   - Right window shows the processed result
4. **Controls**:
   - Process button: Start the object detection
   - Cancel button: Stop the current processing
   - Show Output button: Open the output folder
5. **Status Updates**: Shows processing progress and device information

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
- The application automatically detects and uses the best available device (CUDA, MPS, or CPU)
- Processing time depends on the model size and input type
- The GUI supports both dark and light system themes
- The window is resizable with a minimum size of 800x600

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed correctly
2. Check that you have a compatible GPU if using CUDA
3. Ensure you have sufficient disk space for output files
4. For video processing, make sure you have the necessary codecs installed

## License

[Your License Here] 