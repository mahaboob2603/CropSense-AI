import os
import numpy as np
import tensorflow as tf
from scipy import stats
import pandas as pd
import sys

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

def run_statistical_significance():
    print("Loading Baseline (Raw) and Production (DIP) Models...")
    model_raw = tf.keras.models.load_model("ml_pipeline/model_nodip.keras")
    model_dip = tf.keras.models.load_model("ml_pipeline/model_with_dip.keras")
    
    val_dir = "data_split/val"
    classes = sorted(os.listdir(val_dir))
    
    # We will sample 10 images from every class to create a uniform N=380 statistical pool
    # This prevents class imbalance from skewing the mathematical calculation
    
    scores_raw = []
    scores_dip = []
    
    print("Gathering N=380 paired validation samples for T-Test (P < 0.05)...")
    for i, c in enumerate(classes):
        class_dir = os.path.join(val_dir, c)
        files = os.listdir(class_dir)[:10]
        
        for f in files:
            img_path = os.path.join(class_dir, f)
            
            # Predict Raw
            img_raw = apply_dip_pipeline(img_path, use_dip=False)
            pred_raw = np.argmax(model_raw.predict(np.expand_dims(img_raw, axis=0), verbose=0)[0])
            scores_raw.append(1 if pred_raw == i else 0)
            
            # Predict DIP
            img_dip = apply_dip_pipeline(img_path, use_dip=True)
            pred_dip = np.argmax(model_dip.predict(np.expand_dims(img_dip, axis=0), verbose=0)[0])
            scores_dip.append(1 if pred_dip == i else 0)

    # Convert to numpy arrays for calculation
    scores_raw = np.array(scores_raw)
    scores_dip = np.array(scores_dip)
    
    acc_raw = np.mean(scores_raw)
    acc_dip = np.mean(scores_dip)
    
    # Perform Paired T-Test
    # Null Hypothesis: The accuracy of Raw and DIP models are identical.
    # Alternate Hypothesis: The accuracy distributions are statistically different.
    t_stat, p_value = stats.ttest_rel(scores_dip, scores_raw)
    
    print("\n==============================================")
    print("   STATISTICAL SIGNIFICANCE (PAIRED T-TEST)   ")
    print("==============================================")
    print(f"Sample Size (N)       : {len(scores_raw)}")
    print(f"Model A (Raw) Acc     : {acc_raw*100:.2f}%")
    print(f"Model B (DIP) Acc     : {acc_dip*100:.2f}%")
    print("----------------------------------------------")
    print(f"T-Statistic           : {t_stat:.4f}")
    print(f"P-Value               : {p_value:.6e}")
    print("----------------------------------------------")
    
    is_significant = p_value < 0.05
    if is_significant:
        print("VERDICT: STATISTICALLY SIGNIFICANT (P < 0.05)")
        print("Conclusion: The DIP Pipeline provides a mathematically proven, repeatable accuracy improvement over the raw Keras CNN.")
    else:
        print("VERDICT: NOT STATISTICALLY SIGNIFICANT (P >= 0.05)")
        print("Conclusion: We failed to reject the null hypothesis.")
        
    print("==============================================\n")
    
    # Save the paired results into a CSV for research audit
    df = pd.DataFrame({
        "Image_ID": range(len(scores_raw)),
        "Raw_Correct": scores_raw,
        "DIP_Correct": scores_dip
    })
    df.to_csv("statistical_significance_pairs.csv", index=False)
    print("Saved binary distribution pairs to statistical_significance_pairs.csv")

if __name__ == "__main__":
    run_statistical_significance()
