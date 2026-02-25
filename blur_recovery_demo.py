import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import sys

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

def apply_synthetic_blur(image_path, kernel_size=(15, 15)):
    img_bgr = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    # Apply heavy Gaussian Blur to simulate bad camera focus
    blurred_rgb = cv2.GaussianBlur(img_rgb, kernel_size, 0)
    return img_rgb, blurred_rgb

def prove_blur_recovery():
    print("Loading Baseline (Raw) and Production (DIP) Models...")
    model_raw = tf.keras.models.load_model("ml_pipeline/model_nodip.keras")
    model_dip = tf.keras.models.load_model("ml_pipeline/model_with_dip.keras")
    
    val_dir = "data_split/val"
    classes = sorted(os.listdir(val_dir))
    
    # Select an image that is highly likely to be confused if blurred
    # We will just pick the first image in Apple___Apple_scab or similar
    import glob
    test_files = glob.glob("data_split/val/*/*")
    test_image_path = test_files[0]
    true_class_name = test_image_path.split(os.sep)[-2]
    
    print(f"Testing Blur Robustness on: {true_class_name}")
    
    img_orig, img_blurred = apply_synthetic_blur(test_image_path, kernel_size=(21, 21))
    
    # Save the blurred image temporarily to ingest it via the standard pipelines
    temp_blur_path = "temp_blurred_test.jpg"
    cv2.imwrite(temp_blur_path, cv2.cvtColor(img_blurred, cv2.COLOR_RGB2BGR))
    
    # 1. Feed into Raw Model A (Expect Failure)
    raw_input = apply_dip_pipeline(temp_blur_path, use_dip=False)
    raw_preds = model_raw.predict(np.expand_dims(raw_input, axis=0), verbose=0)[0]
    raw_pred_idx = np.argmax(raw_preds)
    raw_pred_class = classes[raw_pred_idx]
    raw_conf = raw_preds[raw_pred_idx] * 100
    
    # 2. Feed into DIP Model B (Expect Recovery)
    dip_input = apply_dip_pipeline(temp_blur_path, use_dip=True)
    dip_preds = model_dip.predict(np.expand_dims(dip_input, axis=0), verbose=0)[0]
    dip_pred_idx = np.argmax(dip_preds)
    dip_pred_class = classes[dip_pred_idx]
    dip_conf = dip_preds[dip_pred_idx] * 100
    
    # Visual Output Formulation
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 3, 1)
    plt.imshow(img_orig)
    plt.title(f"Ground Truth:\n{true_class_name}")
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(img_blurred)
    color_raw = "green" if raw_pred_class == true_class_name else "red"
    plt.title(f"Model A (Raw) sees Blur\nPredicts: {raw_pred_class}\nConf: {raw_conf:.1f}%", color=color_raw)
    plt.axis('off')
    
    # Calculate exactly what DIP did visually to the blurred image for the 3rd panel
    from ml_pipeline.dip_module import apply_median_filter, apply_clahe, hsv_segmentation, apply_sharpening
    img_dip_recovered = cv2.resize(img_blurred, (224, 224))
    img_dip_recovered = apply_median_filter(img_dip_recovered)
    img_dip_recovered = apply_clahe(img_dip_recovered)
    img_dip_recovered, _ = hsv_segmentation(img_dip_recovered)
    img_dip_recovered = apply_sharpening(img_dip_recovered)
    
    plt.subplot(1, 3, 3)
    plt.imshow(img_dip_recovered)
    color_dip = "green" if dip_pred_class == true_class_name else "red"
    plt.title(f"Model B (DIP) recovers Edges\nPredicts: {dip_pred_class}\nConf: {dip_conf:.1f}%", color=color_dip)
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig("blur_recovery_comparison.png")
    plt.close()
    
    print("\n==========================================")
    print("      BLURRY IMAGE RECOVERY REPORT        ")
    print("==========================================")
    print(f"Ground Truth : {true_class_name}")
    print(f"Raw Model    : {raw_pred_class} ({raw_conf:.1f}%) -> {'CORRECT' if raw_pred_class == true_class_name else 'FAILED'}")
    print(f"DIP Model    : {dip_pred_class} ({dip_conf:.1f}%) -> {'CORRECT' if dip_pred_class == true_class_name else 'FAILED'}")
    print("==========================================")
    print("Saved visual proof to blur_recovery_comparison.png")
    
    if os.path.exists(temp_blur_path):
        os.remove(temp_blur_path)

if __name__ == "__main__":
    prove_blur_recovery()
