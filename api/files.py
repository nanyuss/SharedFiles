import os
from uuid import uuid4
from io import BytesIO
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, StreamingResponse

from core.database import ClusterManagerFiles
from core.schemas.file import FileResponse, UploadResponse, ClustersInfoResponse
from core.data.files_info import GetFileInfo, DeleteFileInfo, GetAllFilesInfo, UploadFileInfo, ClustersInfo

from decouple import config

router = APIRouter(prefix='/api/files')
files_db = ClusterManagerFiles()
MAX_FILE_SIZE = 52428800
AUTHORIZATION = config('AUTHORIZATION')

def verify_auth(auth: str):
    if auth != f"{AUTHORIZATION}":
        raise HTTPException(status_code=401, detail="Sem autorização")

@router.get(
    '/clusters',
    response_model=list[ClustersInfoResponse],
    name=ClustersInfo.name,
    description=ClustersInfo.description,
    responses=ClustersInfo.responses,
    tags= ClustersInfo.tags,
    dependencies=[Depends(verify_auth)]
)
async def get_clusters_status():
    try:
        status = await files_db.get_clusters_status()
        return JSONResponse(content=status)
    except Exception as e:
        return HTTPException(status_code=500, detail=f'Erro ao obter o status das clusters: {str(e)}')

@router.get(
        '/',
        response_model=list[FileResponse],
        name=GetAllFilesInfo.name,
        description=GetAllFilesInfo.description,
        responses=GetAllFilesInfo.responses,
        tags=GetAllFilesInfo.tags,
        dependencies=[Depends(verify_auth)]
    )
async def file_list():
    files = await files_db.get_all_files()
    return JSONResponse(content=files)

@router.post(
        "/upload",
        summary=UploadFileInfo.name,
        description=UploadFileInfo.description,
        responses=UploadFileInfo.responses,
        tags=UploadFileInfo.tags,
        dependencies=[Depends(verify_auth)]
    )
async def upload_file(file: UploadFile = File(), filename: str = Form(None)):
    
    content = await file.read()
    if int(file.size) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="O arquivo ultrapassou o tamanho limite")

    file_id = str(uuid4())
    file_ext = os.path.splitext(file.filename)[1]

    response = files_db.upload_file(
        file_id=file_id + file_ext,
        filename=filename or file.filename,
        content_type=file.content_type,
        file_data=content
    )

    return JSONResponse(content=response)

@router.get(
    "/{file_id}",
    name=GetFileInfo.name,
    description=GetFileInfo.description,
    responses=GetFileInfo.responses,
    tags=GetFileInfo.tags
)
async def get_file(file_id: str):
    try:
        file_info, file_content = files_db.get_file(file_id)
        if not file_info or not file_content:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

        
        file_data = BytesIO(file_content.read())

        response = StreamingResponse(
            file_data,
            media_type=file_info['mimetype'],
            headers={
                'content-Disposition': f'inline; filename="{file_info["filename"]}"'
            }
        )

        return response
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar arquivo: {str(e)}")

@router.delete(
    "/files/{file_id}",
    summary=DeleteFileInfo.name,
    description=DeleteFileInfo.description,
    responses=DeleteFileInfo.responses,
    tags=DeleteFileInfo.tags,
    dependencies=[Depends(verify_auth)]
)
async def delete_file(file_id: str):
    try:
        deleted = files_db.delete_file(file_id)
        if deleted:
            return {"detail": "Arquivo deletado com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado para deletar")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar arquivo: {str(e)}")