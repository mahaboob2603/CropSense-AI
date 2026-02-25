import tensorflow as tf
import os
import numpy as np
import time
from sklearn.metrics import accuracy_score, f1_score
import sys

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

def evaluate_tflite_model(tflite_model_path, val_dir):
    print(f"\n--- Evaluating Quantized TFLite Model ---")
    
    # Initialize TFLite Interpreter
    interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    classes = sorted(os.listdir(val_dir))
    y_true = []
    y_pred = []
    
    # Same subset used in evaluate_dip.py
    for i, c in enumerate(classes):
        class_dir = os.path.join(val_dir, c)
        files = os.listdir(class_dir)[:5]
        
        for f in files:
            img_path = os.path.join(class_dir, f)
            img_array = apply_dip_pipeline(img_path, use_dip=True)
            img_batch = np.expand_dims(img_array, axis=0).astype(np.float32)
            
            interpreter.set_tensor(input_details[0]['index'], img_batch)
            interpreter.invoke()
            preds = interpreter.get_tensor(output_details[0]['index'])[0]
            
            pred_idx = np.argmax(preds)
            y_true.append(i)
            y_pred.append(pred_idx)
            
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')
    
    print(f"INT8 Accuracy: {acc*100:.2f}%")
    print(f"INT8 F1-Score: {f1:.4f}")
    return acc, f1

def quantize_model():
    model_path = "ml_pipeline/model_with_dip.keras"
    output_path = "ml_pipeline/model_edge_quantized.tflite"
    
    print(f"Loading Keras model from {model_path}...")
    model = tf.keras.models.load_model(model_path)

    print("Initializing TFLite Converter...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)

    # Set optimizations for default weight quantization (8-bit hybrid)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    print("Converting to TFLite format (this may take a moment)...")
    tflite_model = converter.convert()

    with open(output_path, "wb") as f:
        f.write(tflite_model)

    raw_size = os.path.getsize(model_path) / (1024 * 1024)
    quant_size = os.path.getsize(output_path) / (1024 * 1024)
    
    print("\nEvaluating Baseline Keras Model for FP32 Reference...")
    # Evaluate Baseline Model (FP32)
    # Re-using the logic from evaluate_dip.py by importing it
    from evaluate_dip import evaluate_pipeline
    acc_fp32, f1_fp32, _ = evaluate_pipeline(model_path, "data_split/val", use_dip=True)
    
    # Evaluate Quantized Model (INT8)
    acc_int8, f1_int8 = evaluate_tflite_model(output_path, "data_split/val")

    print("\n===============================")
    print("   MODEL QUANTIZATION REPORT   ")
    print("===============================")
    print(f"Original Model Size (FP32): {raw_size:.2f} MB")
    print(f"TFLite Edge Size (INT8)   : {quant_size:.2f} MB")
    print(f"Compression Ratio         : ~{raw_size/quant_size:.1f}x smaller")
    print("-------------------------------")
    print(f"FP32 Accuracy  : {acc_fp32*100:.2f}%")
    print(f"INT8 Accuracy  : {acc_int8*100:.2f}%")
    print(f"Accuracy Drop  : {(acc_fp32 - acc_int8)*100:.2f}%")
    print(f"FP32 F1-Score  : {f1_fp32:.4f}")
    print(f"INT8 F1-Score  : {f1_int8:.4f}")
    print("===============================")
    print(f"Saved optimized edge model to: {output_path}")

if __name__ == "__main__":
    quantize_model()
