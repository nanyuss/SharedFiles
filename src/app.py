from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from src.api.files import router

app = FastAPI(
    title='Shared Files',
    version='1.0.0',
    docs_url=None,
    redoc_url=None,
)

@app.get('/', include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_favicon_url='https://i.ibb.co/MnGYv3p/pastas.png'
    )

app.include_router(router.router)