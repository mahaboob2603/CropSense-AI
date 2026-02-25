import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, TensorBoard
import numpy as np
import pandas as pd
from dip_module import apply_dip_pipeline

class CropDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, directory, batch_size=32, use_dip=True, shuffle=True):
        self.directory = directory
        self.batch_size = batch_size
        self.use_dip = use_dip
        self.shuffle = shuffle
        
        self.classes = sorted(os.listdir(directory))
        self.num_classes = len(self.classes)
        self.class_indices = dict(zip(self.classes, range(len(self.classes))))
        
        self.filepaths = []
        self.labels = []
        for c in self.classes:
            c_dir = os.path.join(directory, c)
            if os.path.isdir(c_dir):
                for f in os.listdir(c_dir):
                    self.filepaths.append(os.path.join(c_dir, f))
                    self.labels.append(self.class_indices[c])
                    
        self.indices = np.arange(len(self.filepaths))
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __len__(self):
        return int(np.ceil(len(self.filepaths) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        
        batch_x = []
        batch_y = []
        
        for i in batch_indices:
            try:
                img = apply_dip_pipeline(self.filepaths[i], use_dip=self.use_dip)
                batch_x.append(img)
                batch_y.append(self.labels[i])
            except Exception as e:
                print(f"Error processing {self.filepaths[i]}: {e}")
                
        return np.array(batch_x), tf.keras.utils.to_categorical(batch_y, num_classes=self.num_classes)
        
    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

def build_model(num_classes):
    base_model = MobileNetV3Small(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze base model first
    for layer in base_model.layers:
        layer.trainable = False
        
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def train_model(use_dip=True):
    train_dir = 'data_split/train'
    val_dir = 'data_split/val'
    
    if not os.path.exists(train_dir):
        print("Training directory not found. Please run data_prep.py first.")
        return

    print(f"--- Starting Training Run (USE_DIP={use_dip}) ---")
    train_gen = CropDataGenerator(train_dir, batch_size=32, use_dip=use_dip, shuffle=True)
    val_gen = CropDataGenerator(val_dir, batch_size=32, use_dip=use_dip, shuffle=False)
    
    num_classes = train_gen.num_classes
    model = build_model(num_classes)
    
    model_name = "model_with_dip" if use_dip else "model_without_dip"
    
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True, monitor='val_loss'),
        ReduceLROnPlateau(factor=0.5, patience=3, min_lr=1e-6, monitor='val_loss'),
        ModelCheckpoint(f'{model_name}.keras', save_best_only=True, monitor='val_loss'),
        TensorBoard(log_dir=f'./logs/{model_name}')
    ]
    
    # Normally we do 20+ epochs, but this is a demo/baseline script so we limit it.
    model.fit(train_gen,
              validation_data=val_gen,
              epochs=2, 
              callbacks=callbacks)
              
    print(f"Training finished. Model saved as {model_name}.keras")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-dip', action='store_true', help="Train without DIP")
    args = parser.parse_args()
    
    use_dip = not args.no_dip
    train_model(use_dip=use_dip)
