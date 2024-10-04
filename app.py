from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from api import files

app = FastAPI(
    title='File Upload API',
    version='1.0.0',
    docs_url=None,
    redoc_url=None,
    license_info={
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT'
    }
)

@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_favicon_url='https://i.ibb.co/MnGYv3p/pastas.png'
    )

app.include_router(files.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)