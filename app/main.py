# Updated main.py for Render compatibility

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import subprocess
import uuid

app = FastAPI()

# Allow all CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert_step_file(step_file: UploadFile = File(...)):
    try:
        # Create a unique working directory
        session_id = str(uuid.uuid4())
        input_dir = f"/tmp/input_{session_id}"
        output_dir = f"/tmp/output_{session_id}"
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        input_path = os.path.join(input_dir, step_file.filename)

        # Save uploaded STEP file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(step_file.file, buffer)

        # Call FreeCAD processing script
        result = subprocess.run(
            ["freecadcmd", "convert_to_dxf.py", input_path, output_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return JSONResponse(status_code=500, content={"error": result.stderr})

        # List DXF files generated
        files = [f for f in os.listdir(output_dir) if f.endswith(".dxf")]
        return {"message": "Conversion successful", "files": files}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
