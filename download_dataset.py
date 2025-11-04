import kagglehub
import zipfile
import os
import shutil

data_dir = os.path.join(os.getcwd(), "data")
images_dir = os.path.join(data_dir, "images")

os.makedirs(images_dir, exist_ok=True)

path = kagglehub.dataset_download("vasukipatel/face-recognition-dataset")
print("Downloaded path:", path)

def copy_images(src_dir, dst_dir):
    for filename in os.listdir(src_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)
            shutil.copy(src_file, dst_file)

def copy_images_recursive(src_dir, dst_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                shutil.copy(os.path.join(root, file), dst_dir)

if os.path.isfile(path) and path.endswith(".zip"):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        temp_extract_dir = os.path.join(data_dir, "temp_extract")
        os.makedirs(temp_extract_dir, exist_ok=True)
        zip_ref.extractall(temp_extract_dir)
        print("Extraction complete. Copying images...")
        copy_images(temp_extract_dir, images_dir)
        shutil.rmtree(temp_extract_dir)
        os.remove(path)
elif os.path.isdir(path):
    # Already a folder, copy images
    copy_images(path, images_dir)
else:
    raise Exception(f"Unexpected path type returned: {path}")

print("Dataset ready in:", images_dir)
