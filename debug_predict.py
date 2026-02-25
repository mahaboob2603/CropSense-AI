import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "ml_pipeline")))
import tensorflow as tf
from dip_module import apply_dip_pipeline
from grad_cam import generate_grad_cam_base64
import numpy as np
import traceback

def test():
    try:
        MODEL_PATH = "ml_pipeline/model_with_dip.keras"
        m = tf.keras.models.load_model(MODEL_PATH)
        
        
        # Test 1: Random noise
        img_array1 = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        img_batch1 = np.expand_dims(img_array1, axis=0)
        preds1 = m.predict(img_batch1)[0]
        print("Prediction 1:", np.argmax(preds1))

        # Test 2: An actual image (grab a leaf from the split set)
        import glob
        files = glob.glob("data_split/val/*/*.*")
        if files:
            img2 = apply_dip_pipeline(files[0], use_dip=True)
            img_batch2 = np.expand_dims(img2, axis=0)
            preds2 = m.predict(img_batch2)[0]
            print("Prediction 2:", np.argmax(preds2))
        else:
            print("No real images found for Test 2.")
            
    except Exception as e:
        print("ERROR OCCURRED:")
        print(traceback.format_exc())

if __name__ == "__main__":
    test()
