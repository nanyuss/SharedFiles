from pathlib import Path

upload_dir = Path('./uploads')
upload_dir.mkdir(parents=True, exist_ok=True)

def get_file_path(file_id: str) -> Path:
    return upload_dir / file_id

def get_file_size(file_path: Path) -> int:
    return file_path.stat().st_size

def convert_size(size_bytes: int) -> str:
    """Converte bytes para string legível (MB, KB, GB etc.)."""
    if size_bytes == 0:
        return '0B'

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024
        i += 1
    return f'{size_bytes:.2f}{units[i]}'