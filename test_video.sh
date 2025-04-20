#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run video detection on the sample video
python detect.py --video sample_video/"Sony BRAVIA 7 Youtube 3.m4v"

# Deactivate virtual environment
deactivate 