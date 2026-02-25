import cv2
import numpy as np
import os
import time

def resize_image(image, size=(224, 224)):
    return cv2.resize(image, size)

def apply_production_dip(image_bgr):
    """
    Highly optimized production DIP pipeline (<200ms).
    1. GLI (Green Leaf Index) masking
    2. LAB A-channel Otsu thresholding
    3. Logical AND combination + Morphology
    4. Largest connected component extraction
    """
    start_time = time.time()
    
    # Resize first to reduce processing volume
    img_resized = resize_image(image_bgr, (224, 224))
    
    # 1. GLI (Green Leaf Index)
    # GLI = (2G - R - B) / (2G + R + B)
    # To avoid division by zero and float conversion overhead, we use a simplified ExG-like approach:
    # 2G - R - B > threshold
    b, g, r = cv2.split(img_resized)
    g_16 = g.astype(np.int16)
    r_16 = r.astype(np.int16)
    b_16 = b.astype(np.int16)
    exg = 2 * g_16 - r_16 - b_16
    _, exg_mask = cv2.threshold(np.clip(exg, 0, 255).astype(np.uint8), 20, 255, cv2.THRESH_BINARY)
    
    # 2. LAB A-channel Otsu
    # Green/Red opposition. Lower 'A' values are greener.
    lab = cv2.cvtColor(img_resized, cv2.COLOR_BGR2LAB)
    l, a, b_chan = cv2.split(lab)
    
    # Apply Otsu to find the optimal threshold for separating green from background/red
    otsu_thresh, _ = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Shift threshold slightly toward red to preserve brown/necrotic tissue
    relaxed_thresh = min(otsu_thresh + 10, 255)
    
    # Create the relaxed mask without clipping moderate positive A values
    _, lab_mask = cv2.threshold(a, relaxed_thresh, 255, cv2.THRESH_BINARY_INV)
    
    # 3. Combine Masks (Logical AND)
    combined_mask = cv2.bitwise_and(exg_mask, lab_mask)
    
    # 4. Morphological Cleanup (Close then Open)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_closed = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    mask_opened = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
    
    # 5. Extract Largest Connected Component
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_opened, connectivity=8)
    if num_labels > 1:
        # background is always label 0, so find max area among labels 1..N
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        final_mask = np.where(labels == largest_label, 255, 0).astype(np.uint8)
    else:
        final_mask = mask_opened

    # Slightly dilate the final mask to preserve edge lesions and ensure no necrotic tip clipping
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    final_mask = cv2.dilate(final_mask, kernel_dilate, iterations=1)

    # 6. Apply mask to original image
    segmented_bgr = cv2.bitwise_and(img_resized, img_resized, mask=final_mask)
    
    # Convert BGR to RGB for CNN
    segmented_rgb = cv2.cvtColor(segmented_bgr, cv2.COLOR_BGR2RGB)
    
    # Optional: Mild Unsharp Mask Sharpening
    gaussian = cv2.GaussianBlur(segmented_rgb, (0, 0), 2.0)
    segmented_rgb = cv2.addWeighted(segmented_rgb, 1.5, gaussian, -0.5, 0)
    
    intermediate_masks = {
        "gli": exg_mask,
        "lab": lab_mask,
        "combined": combined_mask
    }
    
    preprocessing_time = (time.time() - start_time) * 1000  # ms
    
    return segmented_rgb, final_mask, preprocessing_time, intermediate_masks


def apply_dip_pipeline(image_path: str, use_dip: bool = True):
    """
    Main entry point for model inference.
    Reads an image from image_path. 
    Always resizes to 224x224 and returns RGB float32 normalized image array.
    """
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise ValueError(f"Could not read image: {image_path}")
        
    start_time = time.time()
    
    if use_dip:
        img_rgb, _, _ = apply_production_dip(img_bgr)
    else:
        # Standard raw resize
        img_rgb = resize_image(img_bgr, size=(224, 224))
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
        
    from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
    
    # img is currently [0, 255] float/uint8, pass it to Keras preprocess
    final_input = preprocess_input(img_rgb.astype(np.float32))
    
    prep_time = (time.time() - start_time) * 1000
    
    return final_input, prep_time
