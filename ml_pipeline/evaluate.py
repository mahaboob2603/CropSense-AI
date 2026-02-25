import os
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
from train import CropDataGenerator

def evaluate_model(model_path, use_dip, test_dir):
    print(f"Evaluating {model_path} (USE_DIP={use_dip})...")
    if not os.path.exists(model_path):
        print(f"Model {model_path} not found. Returning dummy stats.")
        return None, None, None
        
    model = tf.keras.models.load_model(model_path)
    test_gen = CropDataGenerator(test_dir, batch_size=32, use_dip=use_dip, shuffle=False)
    
    y_true = []
    y_pred = []
    y_scores = []
    
    start_time = time.time()
    for i in range(len(test_gen)):
        x, y = test_gen[i]
        preds = model.predict(x, verbose=0)
        y_true.extend(np.argmax(y, axis=1))
        y_pred.extend(np.argmax(preds, axis=1))
        y_scores.extend(preds)
        
    end_time = time.time()
    inference_time_per_image = (end_time - start_time) / len(y_true)
    
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    y_scores = np.array(y_scores)
    
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    
    metrics = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "Inference Time / Img": inference_time_per_image
    }
    
    return metrics, cm, (y_true, y_scores)

def plot_roc(y_true, y_scores, num_classes, model_name):
    y_true_onehot = tf.keras.utils.to_categorical(y_true, num_classes=num_classes)
    plt.figure()
    for i in range(num_classes):
        fpr, tpr, _ = roc_curve(y_true_onehot[:, i], y_scores[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=1, alpha=0.3)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Multi-class ROC - {model_name}')
    plt.savefig(f'roc_{model_name}.png')
    plt.close()

def plot_cm(cm, classes, model_name):
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=False, cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig(f'cm_{model_name}.png')
    plt.close()

def run_evaluation():
    test_dir = 'data_split/test'
    if not os.path.exists(test_dir):
        print("Data split not found.")
        return
        
    classes = sorted(os.listdir(test_dir))
    
    # 1. Model WITH DIP
    metrics_dip, cm_dip, roc_data_dip = evaluate_model('model_with_dip.h5', use_dip=True, test_dir=test_dir)
    if metrics_dip:
        plot_cm(cm_dip, classes, 'model_with_dip')
        plot_roc(roc_data_dip[0], roc_data_dip[1], len(classes), 'model_with_dip')
        
    # 2. Model WITHOUT DIP
    metrics_nodip, cm_nodip, roc_data_nodip = evaluate_model('model_without_dip.h5', use_dip=False, test_dir=test_dir)
    if metrics_nodip:
        plot_cm(cm_nodip, classes, 'model_without_dip')
        plot_roc(roc_data_nodip[0], roc_data_nodip[1], len(classes), 'model_without_dip')

    print("\n========= EVALUATION REPORT =========")
    if metrics_dip:
        print("WITH DIP Pipeline:")
        for k, v in metrics_dip.items():
            print(f"  {k}: {v:.4f}")
    if metrics_nodip:
        print("WITHOUT DIP Pipeline:")
        for k, v in metrics_nodip.items():
            print(f"  {k}: {v:.4f}")

if __name__ == "__main__":
    run_evaluation()
