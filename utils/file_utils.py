from datetime import datetime
from pathlib import Path

def create_output_dir():
    """Create output directory with timestamp inside an 'output' folder"""
    # Create main output directory if it doesn't exist
    main_output_dir = Path("output_results")
    main_output_dir.mkdir(exist_ok=True)
    
    # Create timestamped subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = main_output_dir / f"run_{timestamp}"
    output_dir.mkdir(exist_ok=True)
    return output_dir

def get_image_files(folder_path):
    """Get all image files from a folder"""
    image_extensions = (".jpg", ".jpeg", ".png")
    return [f for f in folder_path.glob("*") if f.suffix.lower() in image_extensions] 