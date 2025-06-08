from fastapi import FastAPI, UploadFile, File
from app.sheet_metal import process_step_file

app = FastAPI()

@app.post("/convert")
async def convert_step(file: UploadFile = File(...)):
    return await process_step_file(file)
