# Face Recognition (DeepFace Workspace)

This repository keeps the DeepFace source inside [`deepface/`](./deepface) and adds local scripts for quick testing.

For full library documentation and advanced usage, see [`deepface/README.md`](./deepface/README.md).

## 1) Prerequisites

- Python 3.10+ recommended
- `pip`
- (Optional) `virtualenv` support via `python -m venv`

## 2) Setup

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ./deepface
```

This follows the same source-install approach as the DeepFace README (`pip install -e .`), adapted to this repo layout.

## 3) Quick Verification Test

Run the local sample script:

```bash
python deepface/match.py
```

It verifies `deepface/img1.jpeg` against `deepface/img2.jpeg` and prints the result.

## 4) Run Server

Start the API server from project root:

```bash
source .venv/bin/activate
python deepface/fast_api.py
```

Or run with uvicorn explicitly:

```bash
source .venv/bin/activate
uvicorn deepface.fast_api:app --host 0.0.0.0 --port 8000
```

Server URL:

- `http://localhost:8000`

Main endpoints:

- `GET /health`
- `POST /match` (accepts base64/data URI images in `img1` and `img2`)

Quick health check:

```bash
curl http://localhost:8000/health
```

## 5) Notes

- First model run may download weights, so internet access may be required.
- If you prefer using DeepFace's original API service scripts, check `deepface/scripts/` and the API section in [`deepface/README.md`](./deepface/README.md).
