"""
Full 38-class training pipeline for CropSense AI.
Extracts archive(3).zip, prepares the data split, and trains both models.
"""
import os
import sys
import zipfile
import shutil
import time

ARCHIVE_PATH = r"c:\Users\mahab\Downloads\archive (3).zip"
PROJECT_ROOT = r"c:\Users\mahab\JARVIs\CropSenseAI"
ML_DIR = os.path.join(PROJECT_ROOT, "ml_pipeline")
TRAIN_DIR = os.path.join(PROJECT_ROOT, "data_split", "train")
VAL_DIR = os.path.join(PROJECT_ROOT, "data_split", "val")

def extract_dataset():
    """Extract the archive and set up proper train/val directories."""
    print("=" * 60)
    print("STEP 1: Extracting archive(3).zip")
    print("=" * 60)
    
    if os.path.exists(TRAIN_DIR):
        existing = os.listdir(TRAIN_DIR)
        if len(existing) >= 38:
            print(f"  Train directory already has {len(existing)} classes. Skipping extraction.")
            return True
        else:
            print(f"  Train directory has only {len(existing)} classes. Re-extracting...")
            shutil.rmtree(os.path.join(PROJECT_ROOT, "data_split"), ignore_errors=True)
    
    if not os.path.exists(ARCHIVE_PATH):
        print(f"  ERROR: Archive not found at {ARCHIVE_PATH}")
        return False
    
    print(f"  Extracting from: {ARCHIVE_PATH}")
    temp_extract = os.path.join(PROJECT_ROOT, "_temp_extract")
    os.makedirs(temp_extract, exist_ok=True)
    
    with zipfile.ZipFile(ARCHIVE_PATH, 'r') as z:
        z.extractall(temp_extract)
    print("  Archive extracted.")
    
    # Find the train and valid directories inside the archive
    # Structure: New Plant Diseases Dataset(Augmented)/train/... 
    #            New Plant Diseases Dataset(Augmented)/valid/...
    aug_dir = None
    for root, dirs, files in os.walk(temp_extract):
        if 'train' in dirs and 'valid' in dirs:
            aug_dir = root
            break
    
    if not aug_dir:
        # Try test directory structure too
        for root, dirs, files in os.walk(temp_extract):
            if 'train' in dirs:
                aug_dir = root
                break
    
    if not aug_dir:
        print("  ERROR: Could not find train/valid directories in archive")
        shutil.rmtree(temp_extract, ignore_errors=True)
        return False
    
    src_train = os.path.join(aug_dir, "train")
    src_val = os.path.join(aug_dir, "valid")
    
    # Copy train
    print(f"  Copying train data from: {src_train}")
    if os.path.exists(src_train):
        shutil.copytree(src_train, TRAIN_DIR)
        train_classes = [d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))]
        total_train = sum(len(os.listdir(os.path.join(TRAIN_DIR, c))) for c in train_classes)
        print(f"  Train: {len(train_classes)} classes, {total_train} images")
    
    # Copy val
    print(f"  Copying validation data from: {src_val}")
    if os.path.exists(src_val):
        shutil.copytree(src_val, VAL_DIR)
        val_classes = [d for d in os.listdir(VAL_DIR) if os.path.isdir(os.path.join(VAL_DIR, d))]
        total_val = sum(len(os.listdir(os.path.join(VAL_DIR, c))) for c in val_classes)
        print(f"  Val: {len(val_classes)} classes, {total_val} images")
    
    # Cleanup
    shutil.rmtree(temp_extract, ignore_errors=True)
    
    print("  Dataset extraction complete!")
    return True


def train_models():
    """Train both DIP and no-DIP models on all 38 classes."""
    sys.path.insert(0, ML_DIR)
    os.chdir(ML_DIR)
    
    # Local imports after path setup
    import numpy as np
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV3Small
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
    from tensorflow.keras.models import Model
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
    from dip_module import apply_dip_pipeline
    
    class CropDataGen(tf.keras.utils.Sequence):
        def __init__(self, directory, batch_size=32, use_dip=True, shuffle=True, limit_per_class=None):
            self.directory = directory
            self.batch_size = batch_size
            self.use_dip = use_dip
            self.shuffle = shuffle
            self.classes = sorted([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))])
            self.num_classes = len(self.classes)
            self.class_indices = {c: i for i, c in enumerate(self.classes)}
            
            self.filepaths = []
            self.labels = []
            for c in self.classes:
                c_dir = os.path.join(directory, c)
                files = sorted(os.listdir(c_dir))
                if limit_per_class:
                    files = files[:limit_per_class]
                for f in files:
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        self.filepaths.append(os.path.join(c_dir, f))
                        self.labels.append(self.class_indices[c])
            
            self.indices = np.arange(len(self.filepaths))
            if self.shuffle:
                np.random.shuffle(self.indices)
            print(f"  Generator: {len(self.filepaths)} images, {self.num_classes} classes, DIP={self.use_dip}")
        
        def __len__(self):
            return int(np.ceil(len(self.filepaths) / self.batch_size))
        
        def __getitem__(self, idx):
            batch_indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
            batch_x, batch_y = [], []
            for i in batch_indices:
                try:
                    img = apply_dip_pipeline(self.filepaths[i], use_dip=self.use_dip)
                    batch_x.append(img)
                    batch_y.append(self.labels[i])
                except Exception:
                    pass
            if not batch_x:
                return np.zeros((1, 224, 224, 3)), tf.keras.utils.to_categorical([0], self.num_classes)
            return np.array(batch_x), tf.keras.utils.to_categorical(batch_y, self.num_classes)
        
        def on_epoch_end(self):
            if self.shuffle:
                np.random.shuffle(self.indices)
    
    def build_model(num_classes):
        base = MobileNetV3Small(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        for layer in base.layers:
            layer.trainable = False
        
        x = base.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.4)(x)
        x = Dense(256, activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.3)(x)
        out = Dense(num_classes, activation='softmax')(x)
        
        model = Model(inputs=base.input, outputs=out)
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model, base
    
    def run_training(use_dip: bool):
        tag = "WITH DIP" if use_dip else "WITHOUT DIP"
        model_filename = "model_with_dip.keras" if use_dip else "model_nodip.keras"
        
        print("\n" + "=" * 60)
        print(f"TRAINING: {tag}")
        print("=" * 60)
        
        # Use up to 200 images per class for training speed
        train_gen = CropDataGen(
            os.path.join(PROJECT_ROOT, "data_split", "train"),
            batch_size=32, use_dip=use_dip, shuffle=True, limit_per_class=200
        )
        val_gen = CropDataGen(
            os.path.join(PROJECT_ROOT, "data_split", "val"),
            batch_size=32, use_dip=use_dip, shuffle=False, limit_per_class=50
        )
        
        model, base = build_model(train_gen.num_classes)
        
        callbacks = [
            EarlyStopping(patience=3, restore_best_weights=True, monitor='val_loss'),
            ReduceLROnPlateau(factor=0.5, patience=2, min_lr=1e-6, monitor='val_loss'),
            ModelCheckpoint(model_filename, save_best_only=True, monitor='val_loss'),
        ]
        
        # Phase 1: Train head only (3 epochs)
        print("\n  Phase 1: Training classification head (base frozen)...")
        model.fit(train_gen, validation_data=val_gen, epochs=3, callbacks=callbacks, verbose=1)
        
        # Phase 2: Fine-tune last 30 layers (3 epochs)
        print("\n  Phase 2: Fine-tuning last 30 layers...")
        for layer in base.layers[-30:]:
            layer.trainable = True
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        callbacks[2] = ModelCheckpoint(model_filename, save_best_only=True, monitor='val_loss')
        model.fit(train_gen, validation_data=val_gen, epochs=3, callbacks=callbacks, verbose=1)
        
        # Also save a copy to project root for backward compat
        root_copy = os.path.join(PROJECT_ROOT, model_filename)
        if os.path.exists(model_filename):
            shutil.copy2(model_filename, root_copy)
        
        print(f"\n  Model saved: {model_filename}")
        return model
    
    # Train both models
    start = time.time()
    dip_model = run_training(use_dip=True)
    nodip_model = run_training(use_dip=False)
    elapsed = time.time() - start
    
    print(f"\n{'=' * 60}")
    print(f"TRAINING COMPLETE in {elapsed/60:.1f} minutes")
    print(f"  model_with_dip.keras → {ML_DIR}")
    print(f"  model_nodip.keras → {ML_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    # Step 1: Extract dataset
    success = extract_dataset()
    if not success:
        print("Dataset extraction failed. Aborting.")
        sys.exit(1)
    
    # Step 2: Train models
    train_models()
