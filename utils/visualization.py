import cv2

def draw_detection(img, box, class_name, conf):
    """Draw bounding box and label on image"""
    x1, y1, x2, y2 = box
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    
    # Draw rectangle
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Create label text
    label = f"{class_name} {conf:.2f}"
    
    # Get text size
    font_scale = 0.8
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_width, text_height), _ = cv2.getTextSize(label, font, font_scale, thickness)
    
    # Calculate text position
    text_x = x1
    text_y = y1 - 10 if y1 - 10 > text_height else y1 + text_height + 10
    
    # Draw background rectangle for text
    cv2.rectangle(img, 
                (text_x, text_y - text_height - 5),
                (text_x + text_width + 5, text_y + 5),
                (0, 255, 0), -1)
    
    # Draw text
    cv2.putText(img, label, (text_x, text_y), font, font_scale, (0, 0, 0), thickness) 