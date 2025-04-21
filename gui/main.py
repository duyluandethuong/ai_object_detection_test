import tkinter as tk
from tkinter import ttk
from pathlib import Path
from ultralytics import YOLO
import utils.device as device_utils
import utils.file_utils as file_utils
import torch
from tqdm import tqdm
import time
import threading
import os
import subprocess
import cv2

from .utils.theme_manager import ThemeManager
from .components.preview_manager import PreviewManager
from .components.control_panel import ControlPanel

class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLOv8 Object Detection")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.root.resizable(width=True, height=True)
        
        # Set macOS-specific window properties
        self.root.tk.call("tk::unsupported::MacWindowStyle", "style", self.root._w, "document", "closeBox")
        
        # Initialize managers
        self.theme_manager = ThemeManager()
        self.preview_manager = PreviewManager(self.root, self.theme_manager)
        self.control_panel = ControlPanel(
            self.root, 
            self.theme_manager,
            self.preview_manager,
            self.process_files,
            self.cancel_processing,
            self.show_output_folder
        )
        
        # Initialize processing state
        self.is_processing = False
        self.should_stop = False
        self.output_dir = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI layout"""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header_frame, text="YOLOv8 Object Detection", 
                style="Title.TLabel").pack(side=tk.LEFT)
        
        # Setup control panel
        self.control_panel.setup_control_panel(main_frame)
        
        # Setup preview frames
        self.preview_manager.setup_preview_frames(main_frame)
        
    def process_files(self):
        """Start processing files"""
        if not self.control_panel.selected_path.get():
            tk.messagebox.showerror("Error", "Please select a file or folder first")
            return
            
        if self.is_processing:
            tk.messagebox.showwarning("Warning", "Processing is already in progress")
            return
            
        if self.control_panel.input_type is None:
            tk.messagebox.showerror("Error", "Invalid input type")
            return
            
        self.is_processing = True
        self.should_stop = False
        self.control_panel.update_status("Processing...")
        self.control_panel.set_processing_state(True)
        
        # Start processing in a separate thread
        threading.Thread(target=self._process_files_thread, daemon=True).start()
        
    def _process_files_thread(self):
        """Process files in a separate thread"""
        try:
            # Get the best available device
            device = device_utils.get_device()
            device_utils.print_device_info(device)
            
            # Update device info in UI
            self.root.after(0, lambda: self.control_panel.update_device_info(device))
            
            # Load selected YOLOv8 model
            model = YOLO(self.control_panel.model_path.get())
            model.to(device)
            
            # Create output directory
            self.output_dir = file_utils.create_output_dir()
            
            # Start timing
            start_time = time.time()
            last_progress_time = time.time()
            processed_frames = 0
            
            if self.control_panel.input_type == 'image':
                image_path = Path(self.control_panel.selected_path.get())
                self.process_image(model, image_path, self.output_dir)
                self.root.after(0, lambda: self.control_panel.update_progress(100))
                
            elif self.control_panel.input_type == 'folder':
                folder_path = Path(self.control_panel.selected_path.get())
                image_files = file_utils.get_image_files(folder_path)
                
                if not image_files:
                    tk.messagebox.showerror("Error", f"No images found in {folder_path}")
                    return
                    
                total_images = len(image_files)
                for i, image_path in enumerate(image_files):
                    if self.should_stop:
                        break
                    self.process_image(model, image_path, self.output_dir)
                    
                    # Update progress
                    progress = (i + 1) / total_images * 100
                    current_time = time.time()
                    if current_time - last_progress_time >= 0.5:  # Update every 0.5 seconds
                        fps = (i + 1) / (current_time - start_time)
                        self.root.after(0, lambda: self.control_panel.update_progress(progress, fps))
                        last_progress_time = current_time
                    
            else:  # video
                video_path = Path(self.control_panel.selected_path.get())
                self.process_video(model, video_path, self.output_dir)
                
            if self.should_stop:
                self.root.after(0, lambda: self.control_panel.update_status("Processing cancelled"))
            else:
                # Calculate and print total processing time
                end_time = time.time()
                total_time = end_time - start_time
                
                device_details = "CPU"
                if device == "cuda":
                    device_details = f"CUDA ({torch.cuda.get_device_name(0)})"
                elif device == "mps":
                    device_details = "MPS (Metal Performance Shaders)"
                    
                self.root.after(0, lambda: self.control_panel.update_status(
                    f"Processing complete!\n"
                    f"Total time: {total_time:.2f} seconds\n"
                    f"Device: {device_details}\n"
                    f"Output saved to: {self.output_dir}"
                ))
                
        except Exception as e:
            self.root.after(0, lambda: tk.messagebox.showerror("Error", f"An error occurred: {str(e)}"))
            self.root.after(0, lambda: self.control_panel.update_status("Processing failed!"))
            
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.control_panel.set_processing_state(False))
            if self.output_dir and self.output_dir.exists():
                self.root.after(0, lambda: self.control_panel.enable_output_button())
                
    def process_image(self, model, image_path, output_dir):
        """Process a single image"""
        if self.should_stop:
            return
            
        # Process single image
        results = model(image_path, verbose=False)
        # Save results
        for r in results:
            im_path = output_dir / f"{image_path.stem}_result{image_path.suffix}"
            r.save(im_path)
            # Update result preview
            self.root.after(0, lambda: self.preview_manager.show_image(str(im_path), 
                                                                    self.preview_manager.result_canvas))
            
    def process_video(self, model, video_path, output_dir):
        """Process a video file"""
        if self.should_stop:
            return
            
        # Process video
        cap = cv2.VideoCapture(str(video_path))
        output_path = output_dir / f"{video_path.stem}_result{video_path.suffix}"
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        # Process frames
        frame_count = 0
        start_time = time.time()
        last_progress_time = time.time()
        
        while cap.isOpened() and not self.should_stop:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process frame
            results = model(frame, verbose=False)
            
            # Get annotated frame
            annotated_frame = results[0].plot()
            
            # Write frame
            out.write(annotated_frame)
            
            # Update preview
            self.root.after(0, lambda: self.preview_manager.update_video_preview(annotated_frame))
            
            # Update progress
            frame_count += 1
            progress = (frame_count / total_frames) * 100
            current_time = time.time()
            if current_time - last_progress_time >= 0.5:  # Update every 0.5 seconds
                processing_fps = frame_count / (current_time - start_time)
                self.root.after(0, lambda: self.control_panel.update_progress(progress, processing_fps))
                last_progress_time = current_time
            
        cap.release()
        out.release()
        
    def cancel_processing(self):
        """Cancel the current processing operation"""
        if self.is_processing:
            self.should_stop = True
            self.control_panel.update_status("Cancelling...")
            self.control_panel.set_processing_state(False)
            
    def show_output_folder(self):
        """Open the output folder in the system file explorer"""
        if self.output_dir and self.output_dir.exists():
            if os.name == 'posix':  # macOS
                subprocess.run(['open', str(self.output_dir)])
            elif os.name == 'nt':  # Windows
                os.startfile(str(self.output_dir))
            else:  # Linux
                subprocess.run(['xdg-open', str(self.output_dir)])

def main():
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 