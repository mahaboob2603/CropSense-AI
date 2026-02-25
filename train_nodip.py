import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model
import numpy as np
import sys

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

class NodipGenerator(tf.keras.utils.Sequence):
    def __init__(self, directory, batch_size=64):
        self.directory = directory
        self.batch_size = batch_size
        self.classes = sorted(os.listdir(directory))
        self.num_classes = len(self.classes)
        self.filepaths = []
        self.labels = []
        for i, c in enumerate(self.classes):
            files = os.listdir(os.path.join(directory, c))
            # Sub-sample data identically to fast_retrain.py
            if "train" in directory:
                files = files[:150]
            else:
                files = files[:30]
                
            for f in files:
                self.filepaths.append(os.path.join(directory, c, f))
                self.labels.append(i)
        
        self.indices = np.arange(len(self.filepaths))
        np.random.shuffle(self.indices)

    def __len__(self):
        return int(np.ceil(len(self.filepaths) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_x = []
        batch_y = []
        for i in batch_indices:
            # THIS IS THE CRUCIAL DIFFERENCE: use_dip=False mapped to variant="none"
            img = apply_dip_pipeline(self.filepaths[i], use_dip=False)
            batch_x.append(img)
            batch_y.append(self.labels[i])
        return np.array(batch_x), tf.keras.utils.to_categorical(batch_y, num_classes=self.num_classes)
        
    def on_epoch_end(self):
        np.random.shuffle(self.indices)

def train_baseline_nodip():
    t_dir = "data_split/train"
    v_dir = "data_split/val"
    
    train_gen = NodipGenerator(t_dir, batch_size=64)
    val_gen = NodipGenerator(v_dir, batch_size=64)
    
    print(f"Training NODIP on {len(train_gen.filepaths)} samples across {train_gen.num_classes} classes...")
    
    base_model = MobileNetV3Small(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    for layer in base_model.layers: layer.trainable = False
        
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x) 
    predictions = Dense(train_gen.num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  loss='categorical_crossentropy', metrics=['accuracy'])
                  
    print("Starting optimized training loop for Baseline (NODIP)...")
    model.fit(train_gen, validation_data=val_gen, epochs=4)
    
    output_path = "ml_pipeline/model_nodip.keras"
    model.save(output_path)
    print(f"Raw Baseline Model (Model A) saved to {output_path}")

if __name__ == "__main__":
    train_baseline_nodip()
