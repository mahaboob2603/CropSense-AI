"""
Phase 10 – Proper Model Retraining
Fixes: Frozen backbone, insufficient epochs, no augmentation, no class weighting.
"""
import os, sys, numpy as np, tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ReduceLROnPlateau
from collections import Counter

sys.path.append(os.path.abspath("ml_pipeline"))
from dip_module import apply_dip_pipeline

class ProperGenerator(tf.keras.utils.Sequence):
    """Generator with proper data augmentation."""
    def __init__(self, directory, batch_size=32, use_dip=True, augment=False):
        self.directory = directory
        self.batch_size = batch_size
        self.use_dip = use_dip
        self.augment = augment
        self.classes = sorted(os.listdir(directory))
        self.num_classes = len(self.classes)
        self.filepaths = []
        self.labels = []
        for i, c in enumerate(self.classes):
            cdir = os.path.join(directory, c)
            files = os.listdir(cdir)
            # Use 300 images/class for training, 50 for val (more data than before)
            if "train" in directory:
                files = files[:300]
            else:
                files = files[:50]
            for f in files:
                self.filepaths.append(os.path.join(cdir, f))
                self.labels.append(i)
        self.indices = np.arange(len(self.filepaths))
        np.random.shuffle(self.indices)

    def __len__(self):
        return int(np.ceil(len(self.filepaths) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_x, batch_y = [], []
        for i in batch_indices:
            try:
                img = apply_dip_pipeline(self.filepaths[i], use_dip=self.use_dip)
                if self.augment:
                    img = self._augment(img)
                batch_x.append(img)
                batch_y.append(self.labels[i])
            except Exception:
                pass
        return np.array(batch_x), tf.keras.utils.to_categorical(batch_y, num_classes=self.num_classes)

    def _augment(self, img):
        """Simple augmentation: random flip, brightness, rotation."""
        if np.random.random() > 0.5:
            img = np.fliplr(img)
        if np.random.random() > 0.5:
            img = np.flipud(img)
        # Random brightness shift (small range since image is already preprocessed to [-1,1])
        img = img + np.random.uniform(-0.1, 0.1)
        img = np.clip(img, -1.0, 1.0)
        return img

    def on_epoch_end(self):
        np.random.shuffle(self.indices)

def compute_class_weights(directory, classes):
    """Compute inverse-frequency class weights for imbalanced data."""
    counts = []
    for c in classes:
        cdir = os.path.join(directory, c)
        counts.append(min(len(os.listdir(cdir)), 300))
    total = sum(counts)
    n_classes = len(classes)
    weights = {}
    for i, count in enumerate(counts):
        weights[i] = total / (n_classes * count) if count > 0 else 1.0
    return weights

def build_model(num_classes):
    """Build MobileNetV3Small with unfrozen last 20 layers."""
    base_model = MobileNetV3Small(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # CRITICAL FIX: Unfreeze the last 20 layers for fine-tuning
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    for layer in base_model.layers[-20:]:
        layer.trainable = True
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    # Lower LR for fine-tuning unfrozen layers
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=3e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train_proper(use_dip=True):
    tag = "DIP" if use_dip else "NODIP"
    output_name = "model_with_dip" if use_dip else "model_nodip"
    
    print(f"\n{'='*50}")
    print(f"  PROPER TRAINING: {tag} MODEL")
    print(f"  Unfrozen layers: 20 | Augmentation: ON | Epochs: 15")
    print(f"{'='*50}\n")
    
    t_dir = "data_split/train"
    v_dir = "data_split/val"
    classes = sorted(os.listdir(t_dir))
    
    train_gen = ProperGenerator(t_dir, batch_size=32, use_dip=use_dip, augment=True)
    val_gen = ProperGenerator(v_dir, batch_size=32, use_dip=use_dip, augment=False)
    
    class_weights = compute_class_weights(t_dir, classes)
    
    print(f"Training: {len(train_gen.filepaths)} samples | Val: {len(val_gen.filepaths)} samples | Classes: {train_gen.num_classes}")
    
    model = build_model(train_gen.num_classes)
    
    trainable_count = sum(1 for l in model.layers if l.trainable)
    print(f"Trainable layers: {trainable_count} / {len(model.layers)}")
    
    callbacks = [
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)
    ]
    
    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=15,
        class_weight=class_weights,
        callbacks=callbacks
    )
    
    path = f"ml_pipeline/{output_name}.keras"
    model.save(path)
    print(f"\n{tag} Model saved to {path}")
    return path

if __name__ == "__main__":
    # Train both models back-to-back
    train_proper(use_dip=True)
    train_proper(use_dip=False)
    print("\nBoth models properly trained. Ready for re-evaluation.")
