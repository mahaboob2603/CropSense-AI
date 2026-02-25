import os
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import sys

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

np.random.seed(42)
tf.random.set_seed(42)

def evaluate_variant(model, val_dir, variant, classes):
    y_true = []
    y_pred = []
    latencies = []
    confidences = []
    
    # Process 5 files per class to keep evaluation speed reasonable for multi-variant passes
    for i, c in enumerate(classes):
        class_dir = os.path.join(val_dir, c)
        files = os.listdir(class_dir)[:5]
        for f in files:
            img_path = os.path.join(class_dir, f)
            t0 = time.time()
            img_array = apply_dip_pipeline(img_path, use_dip=(variant=="full_pipeline"), variant=variant)
            img_batch = np.expand_dims(img_array, axis=0)
            preds = model.predict(img_batch, verbose=0)[0]
            latencies.append((time.time() - t0) * 1000)
            
            pred_idx = np.argmax(preds)
            y_true.append(i)
            y_pred.append(pred_idx)
            confidences.append(preds[pred_idx])
            
    acc = accuracy_score(y_true, y_pred)
    f1_weighted = f1_score(y_true, y_pred, average='weighted')
    f1_macro = f1_score(y_true, y_pred, average='macro')
    f1_per_class = f1_score(y_true, y_pred, average=None)
    avg_latency = np.mean(latencies)
    
    return acc, f1_weighted, f1_macro, f1_per_class, avg_latency, y_true, y_pred, confidences

def plot_disease_wise_metrics(classes, f1_raw, f1_dip):
    df = pd.DataFrame({
        'Disease': classes,
        'Raw Model F1': f1_raw,
        'DIP Model F1': f1_dip,
        'Delta': f1_dip - f1_raw
    })
    df.to_csv('disease_wise_metrics.csv', index=False)
    
    plt.figure(figsize=(15, 8))
    x = np.arange(len(classes))
    width = 0.35
    
    plt.bar(x - width/2, f1_raw, width, label='Raw (Model A)')
    plt.bar(x + width/2, f1_dip, width, label='Full DIP (Model B)')
    
    plt.ylabel('F1-Score')
    plt.title('Disease-Wise F1-Score: Raw vs DIP Pipelining')
    plt.xticks(x, classes, rotation=90, fontsize=8)
    plt.legend()
    plt.tight_layout()
    plt.savefig('disease_wise_metrics.png')
    plt.close()
    print("Saved disease_wise_metrics.png and .csv")

def plot_ablation_study(ablation_results):
    df = pd.DataFrame(ablation_results)
    df.to_csv('dip_ablation_results.csv', index=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Variant', y='Accuracy', palette='viridis')
    plt.title('DIP Pipeline Multi-Variant Ablation Study')
    plt.ylabel('Validation Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('dip_ablation_results.png')
    plt.close()
    print("Saved dip_ablation_results.png and .csv")

def plot_calibration(conf_raw, true_raw, pred_raw, conf_dip, true_dip, pred_dip):
    def expected_calibration_error(y_true, y_pred, conf, num_bins=10):
        bin_boundaries = np.linspace(0, 1, num_bins + 1)
        ece = 0.0
        accs = []
        confs = []
        
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        conf = np.array(conf)
        
        for bin_idx in range(num_bins):
            bin_lower = bin_boundaries[bin_idx]
            bin_upper = bin_boundaries[bin_idx + 1]
            in_bin = np.where((conf > bin_lower) & (conf <= bin_upper))[0]
            if len(in_bin) > 0:
                bin_acc = np.mean(y_true[in_bin] == y_pred[in_bin])
                bin_conf = np.mean(conf[in_bin])
                accs.append(bin_acc)
                confs.append(bin_conf)
                ece += (len(in_bin) / len(y_true)) * np.abs(bin_acc - bin_conf)
            else:
                accs.append(np.nan)
                confs.append(np.nan)
        return ece, bin_boundaries[:-1] + np.diff(bin_boundaries)/2, accs, confs

    ece_raw, bins, accs_raw, confs_raw = expected_calibration_error(true_raw, pred_raw, conf_raw)
    ece_dip, _, accs_dip, confs_dip = expected_calibration_error(true_dip, pred_dip, conf_dip)
    
    plt.figure(figsize=(8, 6))
    plt.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')
    plt.plot(confs_raw, accs_raw, 's-', label=f'Raw Model (ECE: {ece_raw:.3f})')
    plt.plot(confs_dip, accs_dip, 'o-', label=f'DIP Model (ECE: {ece_dip:.3f})')
    plt.xlabel('Confidence')
    plt.ylabel('Accuracy')
    plt.title('Reliability Diagram (Calibration)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('calibration_plot.png')
    plt.close()
    print("Saved calibration_plot.png")

def main():
    val_dir = "data_split/val"
    classes = sorted(os.listdir(val_dir))
    
    print("Loading Models A & B...")
    model_raw = tf.keras.models.load_model("ml_pipeline/model_nodip.keras")
    model_dip = tf.keras.models.load_model("ml_pipeline/model_with_dip.keras")
    
    # 1. Evaluate Baseline Model A (Raw)
    print("\nEvaluating Model A (Raw)...")
    acc_raw, f1_w_raw, f1_m_raw, f1_pc_raw, lat_raw, t_r, p_r, conf_r = evaluate_variant(model_raw, val_dir, "none", classes)
    
    # 2. Disease-Wise & Ablation over Model B (DIP engine)
    variants = ["none", "median_only", "clahe_only", "hsv_mask_only", "median_clahe", "full_pipeline"]
    ablation_results = []
    
    f1_pc_dip_full = None
    t_d, p_d, conf_d = None, None, None
    
    for var in variants:
        print(f"\nEvaluating Model B Variant: {var}...")
        acc, f1_w, f1_m, f1_pc, lat, yt, yp, cf = evaluate_variant(model_dip, val_dir, var, classes)
        ablation_results.append({
            'Variant': var,
            'Accuracy': acc * 100,
            'Macro F1': f1_m,
            'Latency (ms)': lat
        })
        if var == "full_pipeline":
            f1_pc_dip_full = f1_pc
            t_d, p_d, conf_d = yt, yp, cf
            
    # Matrix Plotting is handled by evaluate_dip.py already, but we will output disease_wise metrics
    plot_disease_wise_metrics(classes, f1_pc_raw, f1_pc_dip_full)
    plot_ablation_study(ablation_results)
    plot_calibration(conf_r, t_r, p_r, conf_d, t_d, p_d)
    
    print("\n--- Scientific Evaluation Framework Complete ---")

if __name__ == "__main__":
    main()
