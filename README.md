# Face Recognition & Liveness Detection — Backend (Flask)

This backend service provides **Face Recognition** and **Liveness Detection** APIs using ONNX models and MediaPipe.  
It powers the Flutter mobile app by analyzing image data sent from the frontend.

---

## Project Structure

app/
├── app.py # Main Flask application
├── facetools/ # Face detection, recognition, and liveness modules
├── create_facebank.py # Utility to build the known-face database
├── requirements.txt # Python dependencies
├── Dockerfile # Container setup
└── data/ # Model checkpoints & facebank.csv


---

## ⚙️ Setup

### 1. 🧾 Requirements
- Python 3.12+
- (Optional) Docker
- `data/` folder at project root, containing:
  - `facebank.csv`
  - model checkpoints (ONNX files)

---

### 2. Environment Variables

Create a `.env` file inside `app/`:

```bash
DATA_FOLDER=data
RESNET=inception_resnetv1.onnx
DEEPPIX=OULU_Protocol_2_model_0_0.onnx
FACEBANK=facebank.csv
API_URL=http://localhost:5000
```
---

### 3. Run Locally
```bash
cd app
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt #install dependencies
flask --app app:app run --debug
```
The server will start on: http://localhost:5000

---
## API Endpoints

| Method | Endpoint     | Description                    |
|---------|---------------|--------------------------------|
| POST    | `/main`       | Face recognition + liveness detection |
| POST    | `/identity`   | Identity verification only     |
| POST    | `/liveness`   | Liveness detection only        |

> **Content-Type:** `application/octet-stream`  
> All endpoints expect an image as **raw binary** input.

---

## Example Request

```python
import requests

with open("face.jpg", "rb") as f:
    img = f.read()

resp = requests.post("http://localhost:5000/main", data=img)
print(resp.json())
```

---
## Example Response

```
{
  "message": "Everything is OK.",
  "min_sim_score": 0.79,
  "mean_sim_score": 0.83,
  "liveness_score": 0.97
}
```

---
## Docker Deployment
Deploy easily using Docker:

```
cd app
docker build -t face-backend .
docker run -p 5000:5000 face-backend

```

---
## Features
- Flask-based REST API

- ONNXRuntime for fast model inference

- MediaPipe for accurate face detection

- DeepPixBiS for liveness detection

- ResNet for identity verification

- Spoof logging to data/spoof_log.csv

---

## Project Structure
app/
│
├── main.py                # Flask app entry point
├── models/                # ONNX and deep learning models
├── utils/                 # Helper scripts (face, liveness, identity)
├── data/
│   └── spoof_log.csv      # Log file for spoofing attempts
├── requirements.txt       # Dependencies
└── Dockerfile             # Docker configuration