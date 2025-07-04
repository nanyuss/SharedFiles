from env import ENV


class UploadFileInfo:
    name: str = 'Upload File'
    tags: list[str] = ['Files']
    description: str = (
        'Realiza o upload de um arquivo para o servidor. '
        f'O tamanho máximo permitido é de {int(ENV.MAX_FILE_SIZE) / 1024 / 1024} MB. O arquivo será armazenado no diretório de uploads '
        'e os metadados serão salvos no banco de dados.'
    )
    responses: dict = {
        200: {
            'description': 'Upload realizado com sucesso.',
            'content': {
                'application/json': {
                    'example': {
                        'file_id': 'e8f6a274-c8f1-4b87-919e-24e73e4f6fa6.png',
                        'url': 'http://127.0.0.1/files/e8f6a274-c8f1-4b87-919e-24e73e4f6fa6.png'
                    }
                }
            }
        },
        401: {'description': 'Token de autorização inválido.'},
        400: {'description': 'O arquivo ultrapassou o tamanho limite.'}
    }

    @classmethod
    def to_dict(cls) -> dict:
        """Converte para dicionario"""
        return {
            'name': cls.name,
            'tags': cls.tags,
            'description': cls.description,
            'responses': cls.responses,
        }

class GetAllFilesInfo:
    name: str = 'Get Files'
    tags: list[str] = ['Files']
    description: str = 'Retorna uma lista contendo todos os metadados dos arquivos armazenados.'
    responses: dict = {
        200: {
            'description': 'Lista de arquivos com seus metadados.',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'file_id': '365952d5-3295-475d-9ba4-ac4d080bab0b.png',
                            'filename': 'file.png',
                            'mimetype': 'image/png',
                            'size': '107014',
                            'upload_date': '03-10-2024 23:13:12',
                            'url': 'http://127.0.0.1/files/365952d5-3295-475d-9ba4-ac4d080bab0b.png'
                        }
                    ]
                }
            }
        },
        401: {'description': 'Token de autorização inválido.'}
    }

    @classmethod
    def to_dict(cls) -> dict:
        """Converte para dicionario"""
        return {
            'name': cls.name,
            'tags': cls.tags,
            'description': cls.description,
            'responses': cls.responses,
        }

class GetFileInfo:
    name: str = 'Access File'
    tags: list[str] = ['Files']
    description: str = (
        'Acessa o conteúdo de um arquivo armazenado no servidor com base no ID fornecido.\n\n'
        '⚠️ **Para acessar corretamente, o `file_id` deve incluir a extensão do arquivo.**\n\n'
        'Por exemplo: `365952d5-3295-475d-9ba4-ac4d080bab0b.png`.'
    )
    responses: dict = {
        200: {
            'description': 'Arquivo encontrado.',
            'content': {'application/octet-stream': {}}
        },
        404: {'description': 'Arquivo não encontrado.'}
    }

    @classmethod
    def to_dict(cls) -> dict:
        """Converte para dicionario"""
        return {
            'name': cls.name,
            'tags': cls.tags,
            'description': cls.description,
            'responses': cls.responses,
        }

class DeleteFileInfo:
    name: str = 'Delete File'
    tags: list[str] = ['Files']
    description: str = (
        'Deleta um arquivo armazenado no servidor e seus metadados no banco de dados com base no ID fornecido.\n\n'
        '⚠️ **Para deletar corretamente, o `file_id` deve incluir a extensão do arquivo.**\n\n'
        'Por exemplo: `365952d5-3295-475d-9ba4-ac4d080bab0b.png`.\n\n'
        'O usuário deve fornecer a chave de autorização no cabeçalho da requisição.'
    )
    responses: dict = {
        200: {'description': 'Arquivo deletado com sucesso.'},
        401: {'description': 'Token de autorização inválido.'},
        404: {'description': 'Arquivo não encontrado.'}
    }

    @classmethod
    def to_dict(cls) -> dict:
        """Converte para dicionario"""
        return {
            'name': cls.name,
            'tags': cls.tags,
            'description': cls.description,
            'responses': cls.responses,
        }

class ClustersInfo:
    name: str = 'Clusters Info'
    tags: list[str] = ['Status']
    description: str = 'Retorna as informações de todas as clusters de arquivos, incluindo o armazenamento disponível, total, utilizado, número de arquivos, tipos de arquivos, e dados adicionais de cada cluster.'
    responses: dict = {
        200: {
            'description': 'As informações de status de cada cluster foram recuperadas com sucesso.',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'name': 'Cluster 1',
                            'storage': {
                                'avaliable': '256 MB',
                                'used': '256 MB',
                                'total': '512 MB'
                            },
                            'average_file_size': '2 MB',
                            'files_count': {
                                'by_type': {
                                    'image/jpeg': 50,
                                    'application/pdf': 30,
                                    'video/mp4': 20
                                },
                                'total': 100
                            },
                            'status': 'OK'
                        },
                        {
                            'name': 'Cluster 2',
                            'storage': {
                                'avaliable': '212 MB',
                                'used': '300 MB',
                                'total': '512 MB'
                            },
                            'average_file_size': '2.5 MB',
                            'files_count': {
                                'by_type': {
                                    'image/png': 75,
                                    'application/docx': 40,
                                    'text/plain': 35
                                },
                                'total': 150
                            },
                            'status': 'OK'
                        }
                    ]
                }
            }
        },
        401: {
            'description': 'Token de autorização inválido.'
            },
        404: {
            'description': 'Não é possível obter o status no armazenamento local.'
        },
        500: {
            'description': 'Erro interno no servidor ao tentar recuperar o status das clusters.'
            }
    }

    @classmethod
    def to_dict(cls) -> dict:
        """Converte para dicionario"""
        return {
            'name': cls.name,
            'tags': cls.tags,
            'description': cls.description,
            'responses': cls.responses,
        }