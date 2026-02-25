import tensorflow as tf
from tensorflow.keras.optimizers import Adam
import os
import sys

sys.path.append(os.path.abspath("ml_pipeline"))
from train import CropDataGenerator

def run_finetuning():
    base_dir = "data_split"
    
    # Using the identical custom data generator
    print("Initializing Generators (Subsampled for speed)...")
    train_gen = CropDataGenerator(
        os.path.join(base_dir, 'train'),
        batch_size=32,
        use_dip=True
    )
    val_gen = CropDataGenerator(
        os.path.join(base_dir, 'val'),
        batch_size=32,
        use_dip=True
    )

    model_path = "ml_pipeline/model_with_dip.keras"
    print(f"Loading production model from {model_path}...")
    model = tf.keras.models.load_model(model_path)

    print("Unfreezing the top 20 structural layers for localized fine-tuning...")
    for layer in model.layers[-20:]:
        if not isinstance(layer, tf.keras.layers.BatchNormalization):
            # Safe unfreezing practice: exclude BN layers from unfreezing to prevent momentum mismatch
            layer.trainable = True

    print("Re-compiling with Categorical Focal Cross-Entropy (Alpha=0.25, Gamma=2.0) & LR=1e-5...")
    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss=tf.keras.losses.CategoricalFocalCrossentropy(alpha=0.25, gamma=2.0),
        metrics=['accuracy']
    )

    print("Executing Deep Adaptation Pass (3 Epochs)...")
    model.fit(
        train_gen, 
        validation_data=val_gen, 
        epochs=3, 
        steps_per_epoch=50, 
        validation_steps=10
    )

    output_path = "ml_pipeline/model_with_dip.keras"
    model.save(output_path)
    print(f"Fine-tuning optimization complete. Production weights Overwritten at {output_path}")

if __name__ == "__main__":
    run_finetuning()
