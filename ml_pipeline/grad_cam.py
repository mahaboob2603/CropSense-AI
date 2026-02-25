import numpy as np
import tensorflow as tf
import cv2
import base64
from io import BytesIO
from PIL import Image

def get_img_array(img_path, size=(224, 224)):
    img = tf.keras.utils.load_img(img_path, target_size=size)
    array = tf.keras.utils.img_to_array(img)
    array = np.expand_dims(array, axis=0)
    return array

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        model.inputs, [model.get_layer(last_conv_layer_name).output, model.output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_and_display_gradcam(img_path, heatmap, cam_path="cam.jpg", alpha=0.4):
    img = cv2.imread(img_path)
    if img is None:
        return None
    
    img = cv2.resize(img, (224, 224))

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Resize jet heatmap to match original image dimensions before superposition
    jet = cv2.resize(jet, (img.shape[1], img.shape[0]))

    # Superimpose the heatmap on original image
    superimposed_img = jet * alpha + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)

    # Save the superimposed image
    cv2.imwrite(cam_path, superimposed_img)
    return superimposed_img
    
def generate_grad_cam_base64(img_path, model, last_conv_layer_name):
    try:
        from dip_module import apply_dip_pipeline
        # We need a normalized image array for the model
        img_array = apply_dip_pipeline(img_path, use_dip=True)
        img_array = np.expand_dims(img_array, axis=0) # Batch size 1
        
        # Generate heatmap
        heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)
        
        # Create superimposed image
        cam_bgr = save_and_display_gradcam(img_path, heatmap, alpha=0.5)
        if cam_bgr is None:
            return ""
            
        # Convert to base64
        cam_rgb = cv2.cvtColor(cam_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(cam_rgb)
        buffered = BytesIO()
        pil_img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return "data:image/jpeg;base64," + img_str
    except Exception as e:
        print(f"Error generating Grad-CAM: {e}")
        return ""
