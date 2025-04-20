import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import utils.file_utils as file_utils

class ControlPanel:
    def __init__(self, root, theme_manager, preview_manager, on_process_callback, on_cancel_callback, on_show_output_callback):
        self.root = root
        self.theme_manager = theme_manager
        self.preview_manager = preview_manager
        self.on_process_callback = on_process_callback
        self.on_cancel_callback = on_cancel_callback
        self.on_show_output_callback = on_show_output_callback
        
        # Initialize variables
        self.model_path = tk.StringVar(value="yolov8m.pt")
        self.selected_path = tk.StringVar()
        self.input_type = None
        
    def setup_control_panel(self, parent):
        """Setup the control panel with all controls"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Model selection
        model_frame = ttk.Frame(control_frame)
        model_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(model_frame, text="Model", style="Subtitle.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_path, state="readonly", width=30)
        model_combo['values'] = ("yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt")
        model_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # File selection
        file_frame = ttk.Frame(control_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(file_frame, text="Input", style="Subtitle.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Entry(file_frame, textvariable=self.selected_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(file_frame, text="Browse", command=self.browse_files).pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Process button
        self.process_button = ttk.Button(button_frame, text="Process", 
                                       command=self.on_process_callback, 
                                       style="Accent.TButton")
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        self.cancel_button = ttk.Button(button_frame, text="Cancel", 
                                      command=self.on_cancel_callback, 
                                      style="Danger.TButton", 
                                      state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Output folder button
        self.output_button = ttk.Button(button_frame, text="Show Output", 
                                      command=self.on_show_output_callback, 
                                      state=tk.DISABLED)
        self.output_button.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="", style="Subtitle.TLabel")
        self.status_label.pack(pady=10)
        
        return control_frame
        
    def detect_input_type(self, path):
        """Automatically detect if the path is an image, video, or folder"""
        path = Path(path)
        
        if path.is_file():
            # Check if it's a video file
            video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.m4v', '.webm', '.flv', '.wmv', '.mpg', '.mpeg', '.m4v', '.webm', '.flv', '.wmv', '.mpg', '.mpeg')
            if path.suffix.lower() in video_extensions:
                return 'video'
            
            # Check if it's an image file
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
            if path.suffix.lower() in image_extensions:
                return 'image'
                
        elif path.is_dir():
            # Check if directory contains images
            image_files = file_utils.get_image_files(path)
            if image_files:
                return 'folder'
                
        return None
        
    def browse_files(self):
        """Open file dialog and handle file selection"""
        path = filedialog.askopenfilename(
            title="Select File or Folder",
            filetypes=[
                ("All supported files", "*.jpg *.jpeg *.png *.mp4 *.avi *.mov *.mkv"),
                ("Image files", "*.jpg *.jpeg *.png"),
                ("Video files", "*.mp4 *.avi *.mov *.mkv"),
                ("All files", "*.*")
            ]
        )
        
        if not path:
            return
            
        # Check if the selected path is a directory
        if Path(path).is_dir():
            path = filedialog.askdirectory(initialdir=path)
            if not path:
                return
                
        self.selected_path.set(path)
        self.input_type = self.detect_input_type(path)
        
        if self.input_type is None:
            messagebox.showerror("Error", "Unsupported file type or empty folder")
            return
            
        # Show preview based on input type
        if self.input_type == 'image':
            try:
                self.preview_manager.show_image(path, self.preview_manager.original_canvas)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
        elif self.input_type == 'video':
            try:
                self.preview_manager.show_video_preview(path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load video: {str(e)}")
                
        return self.input_type
        
    def update_status(self, text):
        """Update the status label text"""
        self.status_label.config(text=text)
        
    def set_processing_state(self, is_processing):
        """Update button states based on processing state"""
        self.process_button.config(state=tk.DISABLED if is_processing else tk.NORMAL)
        self.cancel_button.config(state=tk.NORMAL if is_processing else tk.DISABLED)
        self.output_button.config(state=tk.DISABLED if is_processing else tk.NORMAL)
        
    def enable_output_button(self):
        """Enable the output folder button"""
        self.output_button.config(state=tk.NORMAL) 