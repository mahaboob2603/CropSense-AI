import os
import time
import time
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
import sys
import cv2

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

def evaluate_pipeline(model_path, val_dir, use_dip):
    print(f"\n--- Evaluating Model (DIP Enabled: {use_dip}) ---")
    model = tf.keras.models.load_model(model_path)
    
    classes = sorted(os.listdir(val_dir))
    y_true = []
    y_pred = []
    
    latencies = []
    
    # Take a representative sub-sample to benchmark quickly (e.g., 5 files per class)
    for i, c in enumerate(classes):
        class_dir = os.path.join(val_dir, c)
        files = os.listdir(class_dir)[:5]
        
        for f in files:
            img_path = os.path.join(class_dir, f)
            
            start_time = time.time()
            if use_dip:
                img_array = apply_dip_pipeline(img_path, use_dip=True)
            else:
                # Raw processing matching the shape but NOT the DIP transformations
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (224, 224))
                img = preprocess_input(img.astype(np.float32))
                img_array = img
                
            img_batch = np.expand_dims(img_array, axis=0)
            preds = model.predict(img_batch, verbose=0)[0]
            pred_idx = np.argmax(preds)
            
            latency = (time.time() - start_time) * 1000  # ms
            latencies.append(latency)
            
            y_true.append(i)
            y_pred.append(pred_idx)
            
    # Calculate metrics
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')
    cm = confusion_matrix(y_true, y_pred)
    avg_latency = np.mean(latencies)
    
    print(f"Accuracy: {acc*100:.2f}%")
    print(f"F1-Score: {f1:.4f}")
    print(f"Avg End-to-End Latency: {avg_latency:.2f} ms / image")
    
    # Save Confusion Matrix plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(f'Confusion Matrix (DIP Enabled: {use_dip})')
    plt.tight_layout()
    filename = 'confusion_matrix_dip.png' if use_dip else 'confusion_matrix_nodip.png'
    plt.savefig(filename)
    plt.close()
    print(f"Saved confusion matrix to {filename}")
    
    return acc, f1, avg_latency

if __name__ == "__main__":
    val_dir = "data_split/val"
    model_path = "ml_pipeline/model_with_dip.keras"
    
    acc_dip, f1_dip, lat_dip = evaluate_pipeline(model_path, val_dir, use_dip=True)
    acc_nodip, f1_nodip, lat_nodip = evaluate_pipeline(model_path, val_dir, use_dip=False)
    
    print("\n===============================")
    print("      SCIENTIFIC BENCHMARK       ")
    print("===============================")
    print(f"Metric     | With DIP   | Without DIP")
    print(f"-----------|------------|------------")
    print(f"Accuracy   | {acc_dip*100:6.2f}%   | {acc_nodip*100:6.2f}%")
    print(f"F1-Score   | {f1_dip:6.4f}   | {f1_nodip:6.4f}")
    print(f"Latency    | {lat_dip:6.1f} ms | {lat_nodip:6.1f} ms")
    
    with open("benchmark_report.md", "w") as f:
        f.write("# Digital Image Processing (DIP) Benchmark Report\n\n")
        f.write("| Metric | With DIP (OpenCV HSV Masking + CLAHE) | Without DIP (Raw ImageNet Scale) |\n")
        f.write("|---|---|---|\n")
        f.write(f"| **Accuracy** | {acc_dip*100:.2f}% | {acc_nodip*100:.2f}% |\n")
        f.write(f"| **F1-Score** | {f1_dip:.4f} | {f1_nodip:.4f} |\n")
        f.write(f"| **Latency** | {lat_dip:.1f} ms | {lat_nodip:.1f} ms |\n")
    print("\nSaved benchmark report to benchmark_report.md")
