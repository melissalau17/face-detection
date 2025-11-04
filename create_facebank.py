import os
import zipfile
import urllib.request
from pathlib import Path
import csv
import sys

import cv2
import numpy as np
import onnxruntime
from tqdm import tqdm
from facetools import FaceDetection

KAGGLE_DATASET = "vasukipatel/face-recognition-dataset"
DATA_DIR = Path("./data")
IMAGES_DIR = DATA_DIR / "images"
CHECKPOINT_DIR = DATA_DIR / "checkpoints"
CSV_OUTPUT = DATA_DIR / "facebank.csv"
CHECKPOINT_FILE = CHECKPOINT_DIR / "InceptionResnetV1_vggface2.onnx"

for path in [DATA_DIR, IMAGES_DIR, CHECKPOINT_DIR]:
    path.mkdir(parents=True, exist_ok=True)

try:
    import kagglehub
except ImportError:
    os.system("pip install kagglehub")

import kagglehub

print("Downloading Kaggle dataset...")
dataset_zip = kagglehub.dataset_download(KAGGLE_DATASET)
print(f"Downloaded: {dataset_zip}")

if dataset_zip.endswith(".zip"):
    extract_dir = Path(dataset_zip).with_suffix("")  # remove .zip
    print(f"Extracting dataset to {extract_dir} ...")
    with zipfile.ZipFile(dataset_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    dataset_path = extract_dir
else:
    dataset_path = Path(dataset_zip)

print("Copying images to standard folder...")
image_extensions = ("*.jpg", "*.jpeg", "*.png")
for ext in image_extensions:
    for img_path in dataset_path.rglob(ext):
        dest_path = IMAGES_DIR / img_path.name
        if not dest_path.exists():
            dest_path.write_bytes(img_path.read_bytes())

if not CHECKPOINT_FILE.exists():
    print("Downloading InceptionResnetV1 checkpoint...")
    url = "https://github.com/ffletcherr/face-recognition-liveness/releases/download/v0.1/InceptionResnetV1_vggface2.onnx"
    urllib.request.urlretrieve(url, CHECKPOINT_FILE)
    print("Checkpoint downloaded.")

faceDetector = FaceDetection()
resnet = onnxruntime.InferenceSession(str(CHECKPOINT_FILE), providers=["CPUExecutionProvider"])

images_list = []
for ext in image_extensions:
    images_list += list(IMAGES_DIR.glob(ext))

if not images_list:
    print(f"No images found in {IMAGES_DIR}")
    sys.exit()

print("Generating facebank CSV...")
with open(CSV_OUTPUT, "w", newline="") as f:
    writer = csv.writer(f)
    for img_path in tqdm(images_list):
        image = cv2.imread(str(img_path))
        faces, _ = faceDetector(image)
        if not len(faces):
            continue
        face_arr = faces[0]
        face_arr = np.moveaxis(face_arr, -1, 0)
        input_arr = np.expand_dims((face_arr - 127.5) / 128.0, 0)
        embeddings = resnet.run(["output"], {"input": input_arr.astype(np.float32)})[0]
        writer.writerow(embeddings.flatten().tolist())

print(f"facebank CSV created at {CSV_OUTPUT}")
