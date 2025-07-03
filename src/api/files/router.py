import os
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Header, Request
from fastapi.responses import JSONResponse, StreamingResponse

from src.database import DatabaseClient
from .docs import (
    ClustersInfo,
    DeleteFileInfo,
    GetAllFilesInfo,
    UploadFileInfo,
    GetFileInfo
)
from src.schemas.file import (
    ClustersInfoResponse,
    FileResponse,
    UploadResponse
)

from env import ENV

router = APIRouter(prefix='/files')
database = DatabaseClient()

@router.get('/clusters', response_model=list[ClustersInfoResponse], **ClustersInfo.to_dict())
async def get_clusters_status(auth: str = Header()):
    """Retorna as informações de todas as cluster, se o armazenamento for local retorna None"""
    if auth != ENV.AUTHORIZATION_TOKEN:
        raise HTTPException(status_code=401, detail='Sem autorização')

    try:
        if ENV.CLUSTERS:
            status = await database.files.get_clusters_status()
            return JSONResponse(content=status)
        return JSONResponse(status_code=404, content='Não é possível obter o status no armazenamento local.')
    except Exception as e:
        return HTTPException(status_code=500, detail=f'Erro ao obter o status das clusters: {str(e)}')

@router.get('/', response_model= list[FileResponse], **GetAllFilesInfo.to_dict())
async def file_list():
    """Retorna a lista de todos os metadados armazenados"""
    files = await database.files.list_files()
    return JSONResponse(content=files)

@router.post('/upload', response_model=list[UploadResponse], **UploadFileInfo.to_dict())
async def upload_file(request: Request, file: UploadFile = File(), auth: str = Header(), filename: str = Form(None)):
    if auth != ENV.AUTHORIZATION_TOKEN:
        raise HTTPException(status_code=401, detail='Sem autorização')
    
    content = await file.read()
    if int(file.size) > int(ENV.MAX_FILE_SIZE):
        raise HTTPException(status_code=400, detail='O arquivo ultrapassou o tamanho limite')

    file_id = str(uuid4()) + os.path.splitext(file.filename)[1]
    base_url = str(request.base_url).rstrip('/')

    response = database.files.upload_file(
        file_id,
        filename or file.filename,
        file.content_type,
        content,
        base_url
    )

    return JSONResponse(content=response)

@router.get('/{file_id}', **GetFileInfo.to_dict())
async def get_file(file_id: str):
    try:
        file_info, file_content = database.files.get_file(file_id)
        if not file_info or not file_content:
            raise HTTPException(status_code=404, detail='Arquivo não encontrado')

        response = StreamingResponse(
            file_content,
            media_type=file_info['mimetype'],
            headers={
                'content-Disposition': f'inline; filename="{file_info["filename"]}"'
            }
        )

        return response
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao acessar arquivo: {str(e)}')

@router.delete('/{file_id}', **DeleteFileInfo.to_dict())
async def delete_file(file_id: str, auth: str = Header()):
    if auth != ENV.AUTHORIZATION_TOKEN:
        raise HTTPException(status_code=401, detail='Sem autorização')
        
    try:
        deleted = database.files.delete_file(file_id)
        if deleted:
            return {'detail': 'Arquivo deletado com sucesso'}
        else:
            raise HTTPException(status_code=404, detail='Arquivo não encontrado para deletar')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao deletar arquivo: {str(e)}')