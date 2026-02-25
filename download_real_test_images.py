import os
import requests

def download_image(url, filename):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded {filename}")
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")

if __name__ == "__main__":
    test_dir = "real_world_tests"
    os.makedirs(test_dir, exist_ok=True)
    
    print("Fetching real-world domain gap test images...")
    
    # Common real-world examples with messy backgrounds and shadows
    images = {
        "tomato_blight_dirty.jpg": "https://upload.wikimedia.org/wikipedia/commons/2/23/Tomato_leaf_blight.JPG",
        "apple_scab_dirty.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Apple_scab_on_leaf.jpg",
        "grape_black_rot_dirty.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/df/Grape_black_rot_leaf.jpg"
    }
    
    for name, url in images.items():
        download_image(url, os.path.join(test_dir, name))
        
    print("\nTest images saved to ./real_world_tests/")
    print("You can upload these directly via the Next.js UI to verify the confidence/severity systems in real conditions!")
