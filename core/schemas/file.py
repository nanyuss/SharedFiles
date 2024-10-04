from pydantic import BaseModel
from datetime import datetime

class UploadResponse(BaseModel):
    file_id: str
    url: str

class FileResponse(BaseModel):
    file_id: str
    filename: str
    mimetype: str
    size: int
    upload_date: datetime
    content: bytes
    url: str

class ClustersInfoResponse(BaseModel):
    name: str
    storage: dict[str, str]
    avarage_file_size: str
    files_count: int
    status: str