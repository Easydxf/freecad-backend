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
async def convert_step_to_dxf(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    step_path = os.path.join(UPLOAD_DIR, f"{file_id}.step")
    output_dir = os.path.join(UPLOAD_DIR, f"{file_id}_dxf")
    os.makedirs(output_dir, exist_ok=True)

    with open(step_path, "wb") as f:
        f.write(await file.read())

    try:
        result = subprocess.run([
            "FreeCADCmd", "/app/convert_to_dxf.py", step_path, output_dir
        ], capture_output=True, text=True, check=True)

        return {
            "status": "success",
            "message": f"DXFs saved in {output_dir}",
            "logs": result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "details": e.stderr
        }
