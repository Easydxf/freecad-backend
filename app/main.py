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
    output_dir = os.path.join(UPLOAD_DIR, file_id)
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, "wb") as f:
        f.write(file.file.read())

    try:
        result = subprocess.run([
            "FreeCADCmd",
            "/app/convert_to_dxf.py",
            input_path,
            output_dir
        ], check=True, capture_output=True, text=True)

        dxf_files = [
            f for f in os.listdir(output_dir)
            if f.lower().endswith(".dxf")
        ]
        return {
            "filename": file.filename,
            "status": "converted",
            "outputs": dxf_files,
            "logs": result.stdout
        }

    except subprocess.CalledProcessError as e:
        return {
            "error": "Conversion failed",
            "details": e.stderr
        }
