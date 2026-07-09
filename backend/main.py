import os
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Form
from fastapi.responses import FileResponse
import uvicorn
from db import Base, get_db, engine
from ai_evalutor import gemini_chat, writer_ai
from docx_writer import generate_docx
from hashing import hashing_password, verify_password
import users as model
from sqlalchemy.orm import Session
from uuid import uuid4
import jwt

app = FastAPI()

Base.metadata.create_all(bind=engine)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHMM = os.getenv("ALGORITHMM")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}


@app.get("/users", tags=["Users"])
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(model.Users).all()


@app.get("/users/{user_id}", tags=["Users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(model.Users).filter(model.Users.id == user_id).first()


@app.post("/register", tags=["Autentifikatsiya"])
async def register_user(user: model.UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(model.Users).filter(model.Users.email == user.email).first()
    if db_user:
        return {"message": "Email allaqachon ro'yhatdan o'tgan"}
    else:
        new_user = model.Users(
            email=user.email,
            session_id=str(uuid4()),
            password=hashing_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully", "new_user": new_user}


@app.post("/login", tags=["Autentifikatsiya"])
async def login_user(user: model.UsersLogin, db: Session = Depends(get_db)):
    db_user = db.query(model.Users).filter(model.Users.email == user.email).first()
    if not db_user:
        return {"message": "Foydalanuvchi topilmadi"}
    if verify_password(db_user.password, user.password):
        return {"message": "Login successful", "user": db_user}
    else:
        return {"message": "Parol mos kelmadi "}


@app.post("/chat_gemini", tags=["Chat"])
async def chat_gemini(request: model.ChatRequest, db: Session = Depends(get_db)):
    response = gemini_chat(message=request.message, session_id=request.session_id)

    if response['type_input'] == "chat":
        ai_response = response['response']
        file_name = None
    else:
        result_writer = response["result_writer"]
        file_path = generate_docx(
            topic=result_writer["topic"],
            tasks=result_writer["tasks"],
            results=result_writer["results"]
        )
        ai_response = str(result_writer['results'])
        file_name = os.path.basename(file_path)
        response["file_name"] = file_name

    history = model.Chats(
        session_id=request.session_id,
        user_request=request.message,
        ai_response=ai_response
    )
    db.add(history)
    db.commit()

    return response


@app.post("/writer_ai", tags=["Chat"])
async def writer_Ai_chat(reqest: model.ChatRequest, db: Session = Depends(get_db)):
    response = writer_ai(topic=reqest.message)

    file_path = generate_docx(
        topic=response["topic"],
        tasks=response["tasks"],
        results=response["results"]
    )
    file_name = os.path.basename(file_path)
    response["file_name"] = file_name

    history = model.Chats(
        session_id=reqest.session_id,
        user_request=reqest.message,
        ai_response=str(response)
    )
    db.add(history)
    db.commit()
    return response


@app.get("/download_docx/{file_name}", tags=["Chat"])
async def download_docx(file_name: str):
    file_path = os.path.join("./Files", file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")
    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@app.post("/chat_history", tags=["Chat"])
async def get_chat_history(request: model.ChatHistoryRequest, db: Session = Depends(get_db)):
    history = db.query(model.Chats).filter(model.Chats.session_id == request.session_id).all()
    return history


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)