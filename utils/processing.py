import time
import cv2
from pathlib import Path
from .visualization import draw_detection

def process_image(model, image_path, output_dir):
    """Process a single image and save the result"""
    try:
        # Start timing for this image
        image_start_time = time.time()
        
        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Error: Could not read image {image_path}")
            return

        # Perform detection
        results = model(img)
        
        # Track highest confidence detections for each class
        class_detections = {}
        
        # Process all detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                # Get class name and confidence
                cls = int(box.cls[0].cpu().numpy())
                conf = float(box.conf[0].cpu().numpy())
                class_name = model.names[cls]
                
                # Update if this is the highest confidence detection for this class
                if class_name not in class_detections or conf > class_detections[class_name]['conf']:
                    class_detections[class_name] = {
                        'box': (x1, y1, x2, y2),
                        'conf': conf
                    }
        
        # Draw only the highest confidence detection for each class
        for class_name, detection in class_detections.items():
            draw_detection(img, detection['box'], class_name, detection['conf'])

        # Save processed image
        output_path = output_dir / f"processed_{image_path.name}"
        cv2.imwrite(str(output_path), img)
        
        # Calculate and print processing time for this image
        image_processing_time = time.time() - image_start_time
        print(f"\nProcessed {image_path.name}:")
        print(f"  - Time taken: {image_processing_time:.2f} seconds")
        print(f"  - Objects detected: {len(class_detections)}")
        print(f"  - Saved to: {output_path}")
        
    except Exception as e:
        print(f"Error processing image {image_path}: {str(e)}")

def process_video(model, video_path, output_dir):
    """Process a video file and save the result"""
    try:
        # Start timing
        video_start_time = time.time()
        
        # Open video file
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        total_seconds = total_frames / fps

        # Create output video writer
        output_path = output_dir / f"processed_{video_path.name}"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

        print(f"\nProcessing video: {video_path.name}")
        print(f"  - Resolution: {width}x{height}")
        print(f"  - FPS: {fps}")
        print(f"  - Total frames: {total_frames}")
        print(f"  - Duration: {total_seconds:.1f} seconds")

        frame_count = 0
        last_progress_time = time.time()
        progress_interval = 5  # Show progress every 5 seconds

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Perform detection
            results = model(frame)
            
            # Track highest confidence detections for each class
            class_detections = {}
            
            # Process all detections
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Get class name and confidence
                    cls = int(box.cls[0].cpu().numpy())
                    conf = float(box.conf[0].cpu().numpy())
                    class_name = model.names[cls]
                    
                    # Update if this is the highest confidence detection for this class
                    if class_name not in class_detections or conf > class_detections[class_name]['conf']:
                        class_detections[class_name] = {
                            'box': (x1, y1, x2, y2),
                            'conf': conf
                        }
            
            # Draw only the highest confidence detection for each class
            for class_name, detection in class_detections.items():
                draw_detection(frame, detection['box'], class_name, detection['conf'])

            # Write frame to output video
            out.write(frame)
            frame_count += 1

            # Print progress every 5 seconds
            current_time = time.time()
            if current_time - last_progress_time >= progress_interval:
                elapsed_seconds = current_time - video_start_time
                processed_seconds = frame_count / fps
                remaining_seconds = total_seconds - processed_seconds
                progress_percent = (processed_seconds / total_seconds) * 100
                
                print(f"  - Progress: {progress_percent:.1f}% ({processed_seconds:.1f}s / {total_seconds:.1f}s)")
                print(f"  - Elapsed time: {elapsed_seconds:.1f}s")
                print(f"  - Estimated time remaining: {remaining_seconds:.1f}s")
                print(f"  - Current FPS: {frame_count/elapsed_seconds:.1f}")
                last_progress_time = current_time

        # Release resources
        cap.release()
        out.release()

        # Calculate and print processing time
        video_processing_time = time.time() - video_start_time
        print(f"\nVideo processing completed:")
        print(f"  - Time taken: {video_processing_time:.2f} seconds")
        print(f"  - Average FPS: {frame_count/video_processing_time:.2f}")
        print(f"  - Saved to: {output_path}")
        
    except Exception as e:
        print(f"Error processing video {video_path}: {str(e)}") 