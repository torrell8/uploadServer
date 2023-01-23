from fastapi import FastAPI, UploadFile, templating
import aiofiles
import aiofiles.os
from starlette.requests import Request
from starlette.responses import RedirectResponse

app = FastAPI()
templates = templating.Jinja2Templates(directory='static')


@app.post("/upload")
async def upload(file: UploadFile):
    async with aiofiles.open(f"files/{file.filename}", 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    return RedirectResponse("/", status_code=302)


@app.get("/")
async def index(request: Request):
    files = await aiofiles.os.listdir("files")
    return templates.TemplateResponse("index.html", {"request": request, "files": files})
