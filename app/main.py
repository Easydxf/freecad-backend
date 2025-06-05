from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FreeCAD backend!"}

@app.post("/convert")
def convert_file(file: UploadFile = File(...)):
    # placeholder: add your FreeCAD logic here
    return {"filename": file.filename, "status": "processed"}