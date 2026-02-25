import os
import zipfile
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

DATASET_NAME = "emmarex/plantdisease"
DATA_READY_DIR = "dataset/PlantVillage"
TRAIN_DIR = "data_split/train"
VAL_DIR = "data_split/val"
TEST_DIR = "data_split/test"

def download_data():
    if os.path.exists(DATA_READY_DIR):
        print("Dataset directory already exists.")
        return
    print("Please download Kaggle dataset into dataset/PlantVillage properly.")
    return

def generate_synthetic_data():
    print("Generating synthetic dataset (RGB noise) for pipeline validation...")
    import numpy as np
    import cv2
    classes = ["Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
               "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___healthy", "Tomato___Late_blight"]
    
    os.makedirs(DATA_READY_DIR, exist_ok=True)
    for c in classes:
        c_dir = os.path.join(DATA_READY_DIR, c)
        os.makedirs(c_dir, exist_ok=True)
        # Generate 20 images per class
        for i in range(20):
            # Create a 224x224 RGB image with random colors resembling leaves
            img = np.random.randint(0, 150, (224, 224, 3), dtype=np.uint8)
            # Add green bias to make it pass segmentation somewhat
            img[:, :, 1] = np.random.randint(50, 255, (224, 224), dtype=np.uint8)
            cv2.imwrite(os.path.join(c_dir, f"synthetic_{i}.jpg"), img)
    print("Synthetic data generated.")

def clean_data():
    if not os.path.exists(DATA_READY_DIR):
        print(f"{DATA_READY_DIR} not found. Skipping clean.")
        return

    count = 0
    for root, dirs, files in os.walk(DATA_READY_DIR):
        for file in files:
            if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                os.remove(os.path.join(root, file))
                count += 1
    print(f"Removed {count} non-image or invalid files.")

def split_data():
    """Stratified split: 70/15/15"""
    if not os.path.exists(DATA_READY_DIR):
        print("Data dir not found, skip split.")
        return
        
    if os.path.exists(TRAIN_DIR):
        print("Split already exists. Skipping.")
        return

    # Collect all image paths and labels
    filepaths = []
    labels = []
    
    for class_name in os.listdir(DATA_READY_DIR):
        class_dir = os.path.join(DATA_READY_DIR, class_name)
        if os.path.isdir(class_dir):
            for file in os.listdir(class_dir):
                filepaths.append(os.path.join(class_dir, file))
                labels.append(class_name)
                
    df = pd.DataFrame({"filepath": filepaths, "label": labels})
    if len(df) == 0:
        print("No images found.")
        return

    # Count original distribution
    print("Original Distribution:")
    print(df['label'].value_counts())
    df['label'].value_counts().to_csv('original_distribution.csv')
    
    # 70/15/15 split
    train_df, temp_df = train_test_split(df, test_size=0.30, stratify=df['label'], random_state=42)
    val_df, test_df = train_test_split(temp_df, test_size=0.50, stratify=temp_df['label'], random_state=42)
    
    def copy_files(df_split, target_dir):
        os.makedirs(target_dir, exist_ok=True)
        for _, row in df_split.iterrows():
            class_dir = os.path.join(target_dir, row['label'])
            os.makedirs(class_dir, exist_ok=True)
            try:
                shutil.copy2(row['filepath'], os.path.join(class_dir, os.path.basename(row['filepath'])))
            except Exception as e:
                print(f"Error copying {row['filepath']}: {e}")
            
    print("Copying train data...")
    copy_files(train_df, TRAIN_DIR)
    print("Copying val data...")
    copy_files(val_df, VAL_DIR)
    print("Copying test data...")
    copy_files(test_df, TEST_DIR)
    
    print("Data split complete.")

if __name__ == "__main__":
    download_data()
    clean_data()
    split_data()
