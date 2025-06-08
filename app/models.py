from pydantic import BaseModel

class ConversionResponse(BaseModel):
    message: str
    dxf_files: list[str]
