import torch

def get_device():
    """Determine the best available device for processing"""
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

def print_device_info(device):
    """Print information about the device being used"""
    print(f"Using device: {device}")
    if device == "cuda":
        print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
    elif device == "mps":
        print("Using MPS (Metal Performance Shaders)")