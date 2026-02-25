import os
import shutil
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score
import sys

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

def setup_real_world_benchmark():
    src_dir = "real_world_tests"
    dst_dir = "data_split/real_world_benchmark"

    # Strict labeled ground truth corresponding to the Wikipedia scrapes
    mapping = {
        "tomato_blight_dirty.jpg": "Tomato___Early_blight",
        "apple_scab_dirty.jpg": "Apple___Apple_scab",
        "grape_black_rot_dirty.jpg": "Grape___Black_rot"
    }

    if not os.path.exists(src_dir):
        print("real_world_tests directory not found. Please run download_real_test_images.py first.")
        return

    print("Organizing uncurated dirty images into strict Ground Truth label directories...")
    for filename, class_name in mapping.items():
        src_path = os.path.join(src_dir, filename)
        if os.path.exists(src_path):
            class_dir = os.path.join(dst_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)
            shutil.copy(src_path, os.path.join(class_dir, filename))

def evaluate_real_world():
    print("Loading Baseline (Raw) and Production (DIP) Models...")
    model_raw = tf.keras.models.load_model("ml_pipeline/model_nodip.keras")
    model_dip = tf.keras.models.load_model("ml_pipeline/model_with_dip.keras")

    # Load classes from standard train data
    val_dir = "data_split/train"
    classes = sorted(os.listdir(val_dir))

    test_dir = "data_split/real_world_benchmark"
    if not os.path.exists(test_dir):
        return

    y_true = []
    y_pred_raw = []
    y_pred_dip = []

    print(f"Beginning quantitative scoring over messy, unstructured real-world data...")
    for c in os.listdir(test_dir):
        class_dir = os.path.join(test_dir, c)
        if not os.path.isdir(class_dir): continue
        if c not in classes:
            print(f"Warning: Class {c} not found in model schema.")
            continue
        
        class_idx = classes.index(c)

        for f in os.listdir(class_dir):
            img_path = os.path.join(class_dir, f)
            print(f"  -> Testing {f}")

            # 1. Model A Evaluation (Raw CNN)
            img_raw = apply_dip_pipeline(img_path, use_dip=False)
            preds_raw = model_raw.predict(np.expand_dims(img_raw, axis=0), verbose=0)[0]
            y_pred_raw.append(np.argmax(preds_raw))

            # 2. Model B Evaluation (DIP + CNN)
            img_dip = apply_dip_pipeline(img_path, use_dip=True)
            preds_dip = model_dip.predict(np.expand_dims(img_dip, axis=0), verbose=0)[0]
            y_pred_dip.append(np.argmax(preds_dip))

            y_true.append(class_idx)

    acc_raw = accuracy_score(y_true, y_pred_raw)
    acc_dip = accuracy_score(y_true, y_pred_dip)

    print("\n==========================================")
    print("   REAL-WORLD DOMAIN GAP BENCHMARK")
    print("==========================================")
    print(f"Model A (Raw) Accuracy  : {acc_raw*100:.2f}%")
    print(f"Model B (DIP) Accuracy  : {acc_dip*100:.2f}%")
    print("------------------------------------------")
    print(f"Domain Gap Closure Shift: +{(acc_dip - acc_raw)*100:.2f}%")
    print("==========================================\n")

if __name__ == "__main__":
    setup_real_world_benchmark()
    evaluate_real_world()
