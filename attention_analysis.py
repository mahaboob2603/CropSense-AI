import os
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import sys
from scipy.stats import entropy

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

def get_last_conv_layer(model):
    for layer in reversed(model.layers):
        try:
            shape = getattr(layer, "output_shape", None)
            if isinstance(shape, list): shape = shape[0]
            if isinstance(shape, tuple) and len(shape) == 4:
                return layer.name
        except Exception: pass
    return "conv_1"

def generate_heatmap_and_features(model, img_array):
    layer_name = get_last_conv_layer(model)
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(layer_name).output, model.output]
    )
    
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        top_pred_index = tf.argmax(preds[0])
        top_class_channel = preds[:, top_pred_index]
        
    grads = tape.gradient(top_class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    heatmap = heatmap.numpy()
    
    # Extract structural features
    # Activation Energy
    activation_energy = np.mean(last_conv_layer_output.numpy() ** 2)
    
    # Spatial Entropy
    # Normalize heatmap to form a probability distribution
    heatmap_prob = heatmap.flatten() / (np.sum(heatmap.flatten()) + 1e-10)
    spatial_entropy = entropy(heatmap_prob)
    
    return heatmap, activation_energy, spatial_entropy

def perform_attention_analysis():
    print("Loading architecture weights...")
    model_raw = tf.keras.models.load_model("ml_pipeline/model_nodip.keras")
    model_dip = tf.keras.models.load_model("ml_pipeline/model_with_dip.keras")
    
    # Pick a random infected leaf image
    test_image_path = "data_split/val/Tomato___Early_blight/0012b9d2-2130-4a06-a834-b1f3af34f57e___RS_Erly.B 8389.JPG"
    if not os.path.exists(test_image_path):
        # Fallback to any file
        import glob
        test_image_path = glob.glob("data_split/val/*/*")[0]
        
    print(f"Executing Attention Analysis on: {test_image_path}")
    
    # 1. RAW PIPELINE
    img_raw_bgr = cv2.imread(test_image_path)
    img_raw_rgb = cv2.cvtColor(img_raw_bgr, cv2.COLOR_BGR2RGB)
    img_raw_resized = cv2.resize(img_raw_rgb, (224, 224))
    
    # Preprocess identically to how NodipGenerator works
    img_raw_preprocessed = apply_dip_pipeline(test_image_path, use_dip=False)
    img_batch_raw = np.expand_dims(img_raw_preprocessed, axis=0)
    
    # 2. DIP PIPELINE
    img_dip_preprocessed = apply_dip_pipeline(test_image_path, use_dip=True)
    
    # To display the DIP image visually, we reconstruct it from just the DIP steps (no MobileNet preprocess scale)
    img_dip_display = cv2.resize(img_raw_rgb, (224, 224))
    from ml_pipeline.dip_module import apply_median_filter, apply_clahe, hsv_segmentation, apply_sharpening
    img_dip_display = apply_median_filter(img_dip_display)
    img_dip_display = apply_clahe(img_dip_display)
    img_dip_display, _ = hsv_segmentation(img_dip_display)
    img_dip_display = apply_sharpening(img_dip_display)
    
    img_batch_dip = np.expand_dims(img_dip_preprocessed, axis=0)
    
    # Generate Heatmaps and Metrics
    print("Extracting convolutional gradients & entropy tensors...")
    hm_raw, nrg_raw, ent_raw = generate_heatmap_and_features(model_raw, img_batch_raw)
    hm_dip, nrg_dip, ent_dip = generate_heatmap_and_features(model_dip, img_batch_dip)
    
    # Save CSV Outputs
    pd.DataFrame([{
        "Architecture": "Raw Baseline", "Avg Activation Energy": nrg_raw
    }, {
        "Architecture": "DIP Pipeline", "Avg Activation Energy": nrg_dip
    }]).to_csv("attention_energy_comparison.csv", index=False)
    
    pd.DataFrame([{
        "Architecture": "Raw Baseline", "Spatial Heatmap Entropy": ent_raw
    }, {
        "Architecture": "DIP Pipeline", "Spatial Heatmap Entropy": ent_dip
    }]).to_csv("attention_entropy_comparison.csv", index=False)
    
    print("Saved Structural Analytics to CSVs.")
    
    # Overlay heatmaps visually
    hm_raw_resized = cv2.resize(hm_raw, (224, 224))
    hm_raw_Color = cv2.applyColorMap(np.uint8(255 * hm_raw_resized), cv2.COLORMAP_JET)
    hm_raw_Color = cv2.cvtColor(hm_raw_Color, cv2.COLOR_BGR2RGB)
    overlay_raw = cv2.addWeighted(img_raw_resized, 0.6, hm_raw_Color, 0.4, 0)
    
    hm_dip_resized = cv2.resize(hm_dip, (224, 224))
    hm_dip_Color = cv2.applyColorMap(np.uint8(255 * hm_dip_resized), cv2.COLORMAP_JET)
    hm_dip_Color = cv2.cvtColor(hm_dip_Color, cv2.COLOR_BGR2RGB)
    overlay_dip = cv2.addWeighted(img_dip_display, 0.6, hm_dip_Color, 0.4, 0)
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.imshow(img_raw_resized)
    plt.title("Original Raw Image")
    plt.axis('off')
    
    plt.subplot(2, 2, 2)
    plt.imshow(overlay_raw)
    plt.title(f"Model A (Raw) Grad-CAM\nEntropy: {ent_raw:.2f} | Eng: {nrg_raw:.2f}")
    plt.axis('off')
    
    plt.subplot(2, 2, 3)
    plt.imshow(img_dip_display)
    plt.title("DIP Processed Image")
    plt.axis('off')
    
    plt.subplot(2, 2, 4)
    plt.imshow(overlay_dip)
    plt.title(f"Model B (DIP) Grad-CAM\nEntropy: {ent_dip:.2f} | Eng: {nrg_dip:.2f}")
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig("comparison_gradcam.png")
    plt.close()
    print("Visual perception proof saved to comparison_gradcam.png")

if __name__ == "__main__":
    perform_attention_analysis()
