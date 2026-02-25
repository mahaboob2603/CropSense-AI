import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model
import numpy as np
import sys
sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

class OptimizedGenerator(tf.keras.utils.Sequence):
    def __init__(self, directory, batch_size=64): # Increased batch size for more stable gradients
        self.directory = directory
        self.batch_size = batch_size
        self.classes = sorted(os.listdir(directory))
        self.num_classes = len(self.classes)
        self.filepaths = []
        self.labels = []
        for i, c in enumerate(self.classes):
            files = os.listdir(os.path.join(directory, c))
            # Sub-sample data to ensure the model can complete 3 epochs quickly but still see variance
            # Only taking 150 images per class for training speed
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
            img = apply_dip_pipeline(self.filepaths[i], use_dip=True)
            batch_x.append(img)
            batch_y.append(self.labels[i])
        return np.array(batch_x), tf.keras.utils.to_categorical(batch_y, num_classes=self.num_classes)
        
    def on_epoch_end(self):
        np.random.shuffle(self.indices)

def run():
    t_dir = "data_split/train"
    v_dir = "data_split/val"
    
    train_gen = OptimizedGenerator(t_dir, batch_size=64)
    val_gen = OptimizedGenerator(v_dir, batch_size=64)
    
    print(f"Training on {len(train_gen.filepaths)} samples across {train_gen.num_classes} classes...")
    
    # Using larger learning rate to escape local minima, and a much simpler classification tail
    base_model = MobileNetV3Small(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    for layer in base_model.layers: layer.trainable = False
        
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x) 
    # Removed the extra Dense(256) layer entirely to drastically reduce parameters to learn
    predictions = Dense(train_gen.num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Note learning rate 1e-3 (higher than 1e-4)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                  loss='categorical_crossentropy', metrics=['accuracy'])
                  
    print("Starting optimized training loop...")
    # Train for 4 epochs to guarantee it learns features
    model.fit(train_gen, validation_data=val_gen, epochs=4)
    
    # Overwrite the production model
    model.save("ml_pipeline/model_with_dip.keras")
    print("Optimization Complete. Production model updated.")
    
if __name__ == "__main__":
    run()
