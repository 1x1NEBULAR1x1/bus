from typing import Annotated

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from config import DATABASE_URL
from engine import DataBase
import jinja2
import requests

db = DataBase(database_url=DATABASE_URL)
app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get('/')
async def link(key: str | None = None):
    return HTMLResponse((requests.get('http://apirustranss.ru/'+("?key="+key if key else ""))).content)

@app.post("/")
async def receive_data(
    key: Annotated[str, Form()] = None,
    caption: Annotated[str, Form()] = None,
    photo: UploadFile = File(...),
    departure_value: str = Form(...),
    destination_value: str = Form(...),
    price: float = Form(...)
):
    # Преобразуем данные из UploadFile в bytes
    # Формируем данные для отправки
    payload = {
        'departure_value': departure_value,
        'destination_value': destination_value,
        'price': price,
        'key': key,
        'caption': caption,
    }
    files = {'photo': (photo.filename, photo.file.read(), photo.content_type)}
    # Отправляем данные на указанный URL
    target_url = 'http://apirustranss.ru/'
    response = requests.post(target_url, data=payload, files=files)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
