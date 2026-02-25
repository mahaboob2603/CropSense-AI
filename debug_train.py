import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np
import shutil

# Try importing the corrected preprocessing
import sys
sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

def setup_mini_dataset():
    src_dir = "data_split/train"
    val_src = "data_split/val"
    mini_train = "data_split/mini_train"
    mini_val = "data_split/mini_val"
    
    # Let's pick 3 random distinct classes
    classes = sorted(os.listdir(src_dir))[:3]
    print(f"Testing learning across 3 classes: {classes}")
    
    for d in [mini_train, mini_val]:
        if os.path.exists(d): shutil.rmtree(d)
        os.makedirs(d)
        
    for c in classes:
        os.makedirs(os.path.join(mini_train, c))
        os.makedirs(os.path.join(mini_val, c))
        
        # copy 100 train, 30 val
        t_files = os.listdir(os.path.join(src_dir, c))[:100]
        v_files = os.listdir(os.path.join(val_src, c))[:30]
        
        for f in t_files: shutil.copy2(os.path.join(src_dir, c, f), os.path.join(mini_train, c, f))
        for f in v_files: shutil.copy2(os.path.join(val_src, c, f), os.path.join(mini_val, c, f))
    return mini_train, mini_val

class DebugGenerator(tf.keras.utils.Sequence):
    def __init__(self, directory, batch_size=8):
        self.directory = directory
        self.batch_size = batch_size
        self.classes = sorted(os.listdir(directory))
        self.filepaths = []
        self.labels = []
        for i, c in enumerate(self.classes):
            for f in os.listdir(os.path.join(directory, c)):
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
            img = apply_dip_pipeline(self.filepaths[i], use_dip=True)
            batch_x.append(img)
            batch_y.append(self.labels[i])
        return np.array(batch_x), tf.keras.utils.to_categorical(batch_y, num_classes=3)
        
    def on_epoch_end(self):
        np.random.shuffle(self.indices)

def run():
    t, v = setup_mini_dataset()
    train_gen = DebugGenerator(t)
    val_gen = DebugGenerator(v)
    
    base_model = MobileNetV3Small(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    for layer in base_model.layers: layer.trainable = False
        
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(3, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  loss='categorical_crossentropy', metrics=['accuracy'])
                  
    print("Starting fast compilation test...")
    model.fit(train_gen, validation_data=val_gen, epochs=3)
    
    # Test collapse
    print("--- Testing Output Variability ---")
    val_files = [os.path.join(v, os.listdir(v)[0], os.listdir(os.path.join(v, os.listdir(v)[0]))[0]),
                 os.path.join(v, os.listdir(v)[1], os.listdir(os.path.join(v, os.listdir(v)[1]))[0])]
    
    for f in val_files:
        img = np.expand_dims(apply_dip_pipeline(f), axis=0)
        p = model.predict(img)[0]
        print(f"Probabilities for {f}: {np.round(p, 3)} -> Class {np.argmax(p)}")
        
if __name__ == "__main__":
    run()
