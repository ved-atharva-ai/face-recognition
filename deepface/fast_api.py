import base64
import binascii
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from deepface import DeepFace, __version__


app = FastAPI(
    title="DeepFace FastAPI",
    version=__version__,
    description="Face verification API that accepts 2 base64 images.",
)


class VerifyBase64Request(BaseModel):
    img1: str = Field(..., description="Image 1 as data URI or raw base64")
    img2: str = Field(..., description="Image 2 as data URI or raw base64")


def _normalize_base64_image(raw_image: str, field_name: str) -> str:
    image = (raw_image or "").strip()
    if not image:
        raise HTTPException(status_code=422, detail=f"'{field_name}' cannot be empty")
    image = image.replace(" ", "+")
    if image.startswith("data:image/"):
        return image
    try:
        decoded = base64.b64decode(image, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail=f"'{field_name}' must be a valid base64 string or data URI",
        ) from exc

    if decoded.startswith(b"\x89PNG\r\n\x1a\n"):
        mime_type = "image/png"
    elif decoded.startswith(b"\xff\xd8\xff"):
        mime_type = "image/jpeg"
    else:
        raise HTTPException(
            status_code=422,
            detail=f"'{field_name}' must be a PNG or JPEG image",
        )

    return f"data:{mime_type};base64,{image}"


def _verify(img1: str, img2: str) -> Dict[str, Any]:
    try:
        img1_data_uri = _normalize_base64_image(img1, "img1")
        img2_data_uri = _normalize_base64_image(img2, "img2")
        return DeepFace.verify(
            img1_path=img1_data_uri,
            img2_path=img2_data_uri,
            model_name="VGG-Face",
            detector_backend="opencv",
            distance_metric="cosine",
            enforce_detection=False,
            align=True,
            anti_spoofing=False,
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Verification failed: {exc}") from exc


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/match")
def match(payload: VerifyBase64Request) -> Dict[str, Any]:
    return _verify(img1=payload.img1, img2=payload.img2)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fast_api:app", host="0.0.0.0", port=8000, reload=False)
