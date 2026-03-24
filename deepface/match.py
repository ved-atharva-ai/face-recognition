from pathlib import Path

from deepface import DeepFace

base_dir = Path(__file__).resolve().parent
img1_path = base_dir / "img1.jpeg"
img2_path = base_dir / "img2.jpeg"

result: dict = DeepFace.verify(
    img1_path=str(img1_path),
    img2_path=str(img2_path),
    enforce_detection=False,
)

print(result)
