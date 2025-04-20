import tkinter as tk
from PIL import Image, ImageTk
import cv2
from pathlib import Path

class PreviewManager:
    def __init__(self, root, theme_manager):
        self.root = root
        self.theme_manager = theme_manager
        self.current_image = None
        self.current_result = None
        self.video_capture = None
        
    def setup_preview_frames(self, parent):
        """Setup the preview frames and canvases"""
        # Preview section
        preview_frame = tk.Frame(parent)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Original preview
        original_frame = tk.Frame(preview_frame)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(original_frame, text="Original", font=('SF Pro Display', 12)).pack(pady=5)
        self.original_canvas = tk.Canvas(original_frame, 
                                       bg=self.theme_manager.get_theme_color("canvas"),
                                       highlightthickness=0)
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Result preview
        result_frame = tk.Frame(preview_frame)
        result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(result_frame, text="Result", font=('SF Pro Display', 12)).pack(pady=5)
        self.result_canvas = tk.Canvas(result_frame, 
                                     bg=self.theme_manager.get_theme_color("canvas"),
                                     highlightthickness=0)
        self.result_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        return preview_frame
        
    def clear_previews(self):
        """Clear both preview canvases"""
        self.original_canvas.delete("all")
        self.result_canvas.delete("all")
        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None
            
    def show_image(self, image_path, canvas):
        """Display an image in the specified canvas"""
        try:
            image = Image.open(image_path)
            # Store reference to current image
            if canvas == self.original_canvas:
                self.current_image = image_path
            else:
                self.current_result = image_path
                
            # Resize image to fit canvas while maintaining aspect ratio
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            canvas.image = photo  # Keep reference
            canvas.create_image(canvas_width//2, canvas_height//2, image=photo, anchor=tk.CENTER)
        except Exception as e:
            raise Exception(f"Failed to load image: {str(e)}")
            
    def show_video_preview(self, video_path):
        """Display video preview in the original canvas"""
        self.video_capture = cv2.VideoCapture(video_path)
        if not self.video_capture.isOpened():
            raise Exception("Failed to open video file")
            
        def update_preview():
            if self.video_capture is None:
                return
                
            ret, frame = self.video_capture.read()
            if ret:
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert to PIL Image
                image = Image.fromarray(frame)
                # Resize
                canvas_width = self.original_canvas.winfo_width()
                canvas_height = self.original_canvas.winfo_height()
                image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(image)
                self.original_canvas.image = photo
                self.original_canvas.create_image(canvas_width//2, canvas_height//2, 
                                                image=photo, anchor=tk.CENTER)
                
                # Schedule next update
                self.root.after(30, update_preview)
            else:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.root.after(30, update_preview)
                
        update_preview()
        
    def update_video_preview(self, frame):
        """Update the result canvas with a processed video frame"""
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert to PIL Image
        image = Image.fromarray(frame)
        # Resize
        canvas_width = self.result_canvas.winfo_width()
        canvas_height = self.result_canvas.winfo_height()
        image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(image)
        self.result_canvas.image = photo
        self.result_canvas.create_image(canvas_width//2, canvas_height//2, 
                                      image=photo, anchor=tk.CENTER) 