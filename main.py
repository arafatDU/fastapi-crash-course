from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, SQLModel, create_engine, Session, select

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# SQL class for SQLite
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str = Field(default=None, unique=True)
    age: int | None = Field(default=None, index=True)
    password: str = Field(default=None, min_length=8)
    is_active: bool = Field(default=True)



class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
    
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
    
    
@app.post("/questions/")
async def create_question(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        db.add(db_choice)
    db.commit()
    
    
@app.get("/questions/{question_id}")
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result


@app.get("/choices/{question_id}")
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices not found")
    return result
    
    
    

# SQLite database setup
# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, connect_args=connect_args)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)
    

# def get_session():
#     with Session(engine) as session:
#         yield session
        
# SessionDep = Annotated[Session, Depends(get_session)]


# @app.on_event("startup")
# async def on_startup():
#     create_db_and_tables()


# @app.post("/users/")
# def create_user(user: User, session: SessionDep):
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user

# @app.get("/users/")
# def read_users(session: SessionDep) -> List[User]:
#     users = session.exec(select(User)).all()
#     return users

# @app.get("/users/{user_id}")
# def read_user(user_id: int, session: SessionDep):
#     user = session.get(User, user_id)
#     if user:
#         return user
#     return {"error": "User not found"}

# @app.put("/users/{user_id}")
# def update_user(user_id: int, user: User, session: SessionDep):
#     db_user = session.get(User, user_id)
#     if db_user:
#         db_user.name = user.name
#         db_user.email = user.email
#         db_user.age = user.age
#         db_user.password = user.password
#         db_user.is_active = user.is_active
#         session.commit()
#         session.refresh(db_user)
#         return db_user
#     return {"error": "User not found"}

# @app.delete("/users/{user_id}")
# def delete_user(user_id: int, session: SessionDep):
#     user = session.get(User, user_id)
#     if user:
#         session.delete(user)
#         session.commit()
#         return {"message": "User deleted"}
#     return {"error": "User not found"}



# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"}
