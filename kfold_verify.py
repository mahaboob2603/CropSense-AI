import os
import glob
import numpy as np
import tensorflow as tf
from sklearn.model_selection import StratifiedKFold
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model
import pandas as pd
import sys

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

# We sample 25 images per class across 38 classes (950 images) to make 3-folds feasible to process dynamically
class FastKFoldGenerator(tf.keras.utils.Sequence):
    def __init__(self, x_paths, y_labels, batch_size=32):
        self.x_paths = np.array(x_paths)
        self.y_labels = np.array(y_labels)
        self.batch_size = batch_size
        self.indices = np.arange(len(self.x_paths))
        np.random.shuffle(self.indices)

    def __len__(self):
        return int(np.ceil(len(self.x_paths) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_x = []
        batch_y = []
        for i in batch_indices:
            # Strictly evaluate the production DIP architecture
            img = apply_dip_pipeline(self.x_paths[i], use_dip=True)
            batch_x.append(img)
            batch_y.append(self.y_labels[i])
        return np.array(batch_x), tf.keras.utils.to_categorical(batch_y, num_classes=38)

    def on_epoch_end(self):
        np.random.shuffle(self.indices)

def build_compiler():
    base_model = MobileNetV3Small(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    for layer in base_model.layers: layer.trainable = False
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x) 
    predictions = Dense(38, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def run_kfold():
    print("Gathering balanced generic dataset for Stratified 3-Fold Cross-Validation...")
    base_dir = "data_split/train"
    classes = sorted(os.listdir(base_dir))
    
    X_all = []
    Y_all = []
    
    for i, c in enumerate(classes):
        class_dir = os.path.join(base_dir, c)
        files = os.listdir(class_dir)[:25] # 25 images * 38 classes = 950 images
        for f in files:
            X_all.append(os.path.join(class_dir, f))
            Y_all.append(i)
            
    X_all = np.array(X_all)
    Y_all = np.array(Y_all)
    
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    fold_accuracies = []
    
    for fold, (train_idx, val_idx) in enumerate(skf.split(X_all, Y_all)):
        print(f"\n==============================================")
        print(f"   STARTING FOLD {fold + 1} / 3               ")
        print(f"==============================================")
        
        X_train, X_val = X_all[train_idx], X_all[val_idx]
        Y_train, Y_val = Y_all[train_idx], Y_all[val_idx]
        
        train_gen = FastKFoldGenerator(X_train, Y_train, batch_size=32)
        val_gen = FastKFoldGenerator(X_val, Y_val, batch_size=32)
        
        model = build_compiler()
        
        # Train dynamically on the generic fold split
        history = model.fit(train_gen, validation_data=val_gen, epochs=3, verbose=1)
        
        val_acc = history.history['val_accuracy'][-1]
        fold_accuracies.append(val_acc * 100)
        print(f"Fold {fold + 1} Validation Accuracy: {val_acc*100:.2f}%")
        
    print("\n==============================================")
    print("   3-FOLD CROSS-VALIDATION RESULTS            ")
    print("==============================================")
    for i, acc in enumerate(fold_accuracies):
        print(f"Fold {i+1} : {acc:.2f}%")
    print("----------------------------------------------")
    mean_acc = np.mean(fold_accuracies)
    std_acc = np.std(fold_accuracies)
    print(f"Mean Accuracy : {mean_acc:.2f}%")
    print(f"Std Deviation : ±{std_acc:.2f}%")
    print("==============================================\n")
    
    pd.DataFrame({
        "Fold": [1, 2, 3],
        "Validation_Accuracy": fold_accuracies
    }).to_csv("kfold_results.csv", index=False)
    
    print("Saved Stratified Bounds to kfold_results.csv")

if __name__ == "__main__":
    run_kfold()
