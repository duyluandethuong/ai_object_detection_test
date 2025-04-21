import time
import cv2
from pathlib import Path
from tqdm import tqdm
from .visualization import draw_detection

def process_image(model, image_path, output_dir):
    """Process a single image and save the result"""
    try:
        # Start timing for this image
        image_start_time = time.time()
        
        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            tqdm.write(f"Error: Could not read image {image_path}")
            return

        # Perform detection
        results = model(img, verbose=False)
        
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
        tqdm.write(f"\nProcessed {image_path.name}:")
        tqdm.write(f"  - Time taken: {image_processing_time:.2f} seconds")
        tqdm.write(f"  - Objects detected: {len(class_detections)}")
        tqdm.write(f"  - Saved to: {output_path}")
        
    except Exception as e:
        tqdm.write(f"Error processing image {image_path}: {str(e)}")

def process_video(model, video_path, output_dir, progress_bar=True):
    """Process a video file and save the result"""
    try:
        # Start timing
        video_start_time = time.time()
        
        # Open video file
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            tqdm.write(f"Error: Could not open video {video_path}")
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

        tqdm.write(f"\nProcessing video: {video_path.name}")
        tqdm.write(f"  - Resolution: {width}x{height}")
        tqdm.write(f"  - FPS: {fps}")
        tqdm.write(f"  - Total frames: {total_frames}")
        tqdm.write(f"  - Duration: {total_seconds:.1f} seconds")

        frame_count = 0
        last_progress_time = time.time()
        progress_interval = 5  # Show progress every 5 seconds

        # Create progress bar
        pbar = tqdm(total=total_frames, desc="Processing video", unit="frames", position=0, leave=True)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Perform detection
            results = model(frame, verbose=False)
            
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
            pbar.update(1)

            # Update progress info every 5 seconds
            current_time = time.time()
            if current_time - last_progress_time >= progress_interval:
                elapsed_seconds = current_time - video_start_time
                processed_seconds = frame_count / fps
                remaining_seconds = total_seconds - processed_seconds
                current_fps = frame_count/elapsed_seconds
                
                pbar.set_postfix({
                    'FPS': f'{current_fps:.1f}',
                    'ETA': f'{remaining_seconds:.1f}s'
                })
                last_progress_time = current_time

        # Close progress bar
        pbar.close()

        # Release resources
        cap.release()
        out.release()

        # Calculate and print processing time
        video_processing_time = time.time() - video_start_time
        tqdm.write(f"\nVideo processing completed:")
        tqdm.write(f"  - Time taken: {video_processing_time:.2f} seconds")
        tqdm.write(f"  - Average FPS: {frame_count/video_processing_time:.2f}")
        tqdm.write(f"  - Saved to: {output_path}")
        
    except Exception as e:
        tqdm.write(f"Error processing video {video_path}: {str(e)}") 