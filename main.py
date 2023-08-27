from pathlib import Path

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from src.routes import notes, tags, auth
import os

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from src.conf.config import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


api_key = os.environ.get('API_KEY')



app = FastAPI()
app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(notes.router, prefix='/api')



@app.on_event("startup")
async def startup():
    """
    The startup function is called when the server starts up.
    It's a good place to initialize things that are needed by your application,
    such as database connections or background tasks.
    
    :return: A coroutine, so we need to use the await keyword
    :doc-author: Trelent
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)



@app.get("/")
def read_root():
    """
    The read_root function returns a JSON object with the key &quot;message&quot; and the value &quot;Hello World&quot;.
    
    
    :return: A dictionary with the key &quot;message&quot; and the value &quot;hello world&quot;
    :doc-author: Trelent
    """
    return {"message": "Hello World"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)




class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME="cl9bix@meta.ua",
    MAIL_PASSWORD="1103Yk78",
    MAIL_FROM="cl9bix@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Yuriy Klyap",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

app = FastAPI()


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    """
    The send_in_background function is a FastAPI endpoint that accepts an email address and sends an email to it.
    It uses the BackgroundTasks module to send the message in a background thread, so that it doesn't block the main thread.
    
    
    :param background_tasks: BackgroundTasks: Add a task to the background
    :param body: EmailSchema: Get the email address from the request body
    :return: A dictionary with a message
    :doc-author: Trelent
    """
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}
"""
    Відправка email у фоновому режимі.

    :param background_tasks: Об'єкт для додавання фонових завдань.
    :type background_tasks: BackgroundTasks
    :param body: Об'єкт EmailSchema з емейлом отримувача.
    :type body: EmailSchema
    :return: Результат відправки email.
    :rtype: dict
"""

origins = [ 
    "http://localhost:3000"
    ]
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)








if __name__ == '__main__':
        uvicorn.run("main:app", host="localhost", reload=True, log_level="info")


