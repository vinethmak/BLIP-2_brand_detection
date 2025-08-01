from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.brand_detector import detect_brand
from PIL import Image
import shutil, os

router = APIRouter()

UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/")
def root():
    return {"message": "Brand Detection API is running."}


@router.post("/detect-brand/")
async def detect_brand_api(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    finally:
        file.file.close()  # Ensure upload is closed

    try:
        # Run brand detection
        brand_name = detect_brand(file_path)
        return {"brand": brand_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brand detection failed: {e}")
    finally:
        # Clean up image after processing
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                print(f"Cleanup failed: {cleanup_error}")
