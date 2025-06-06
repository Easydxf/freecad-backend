# Canvas document: FreeCAD_SheetMetal_Backend
# File: main.py
import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

# Allow CORS for testing purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "/tmp/uploads"
OUTPUT_DIR = "/tmp/outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/convert")
async def convert_step_to_dxf(step_file: UploadFile = File(...)):
    # Save uploaded STEP file
    unique_id = str(uuid.uuid4())
    step_path = os.path.join(UPLOAD_DIR, f"{unique_id}.step")
    with open(step_path, "wb") as f:
        shutil.copyfileobj(step_file.file, f)

    # Create output folder for this conversion
    output_folder = os.path.join(OUTPUT_DIR, unique_id)
    os.makedirs(output_folder, exist_ok=True)

    # Call the conversion script as a subprocess
    try:
        result = subprocess.run(
            ["python3", "convert_to_dxf.py", step_path, output_folder],
            capture_output=True,
            text=True,
            check=True,
            input="n\n"  # auto choose default face, disables prompts
        )
    except subprocess.CalledProcessError as e:
        return JSONResponse(status_code=500, content={"error": "Conversion failed", "details": e.stderr})

    # Collect generated DXF files
    dxf_files = [f for f in os.listdir(output_folder) if f.endswith(".dxf")]
    if not dxf_files:
        return JSONResponse(status_code=500, content={"error": "No DXF files generated."})

    return {"message": "Conversion successful", "files": dxf_files}
