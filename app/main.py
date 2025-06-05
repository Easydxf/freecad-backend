from fastapi import FastAPI, UploadFile, File
import uvicorn  # Required for local/dev running

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FreeCAD backend!"}

@app.post("/convert")
def convert_file(file: UploadFile = File(...)):
    # placeholder: add your FreeCAD logic here
    return {"filename": file.filename, "status": "processed"}

# Only run uvicorn if this script is run directly (not when imported)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

