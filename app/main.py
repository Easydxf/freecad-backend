from fastapi import FastAPI, UploadFile, File
import os
import uuid
import subprocess

app = FastAPI()

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Hello from FreeCAD backend!"}

@app.post("/convert")
def convert_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}.step")
    output_path = os.path.join(UPLOAD_DIR, f"{file_id}.dxf")

    with open(input_path, "wb") as f:
        f.write(file.file.read())

    try:
        result = subprocess.run([
            "FreeCADCmd",
            "/app/app/convert_to_dxf.py",
            input_path,
            output_path
        ], check=True, capture_output=True, text=True)

        return {
            "filename": file.filename,
            "status": "converted",
            "output": output_path,
            "logs": result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            "error": "Conversion failed",
            "details": e.stderr
        }
