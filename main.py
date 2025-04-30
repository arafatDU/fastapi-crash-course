from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, SQLModel, create_engine, Session, select


app = FastAPI()

class Tea(BaseModel):
    id: int
    name: str
    origin: str 
    
teas: List[Tea] = []



# SQL class for SQLite
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str = Field(default=None, unique=True)
    age: int | None = Field(default=None, index=True)
    password: str = Field(default=None, min_length=8)
    is_active: bool = Field(default=True)


# SQLite database setup
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.post("/users/")
def create_user(user: User, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/")
def read_users(session: SessionDep) -> List[User]:
    users = session.exec(select(User)).all()
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if user:
        return user
    return {"error": "User not found"}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, session: SessionDep):
    db_user = session.get(User, user_id)
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db_user.age = user.age
        db_user.password = user.password
        db_user.is_active = user.is_active
        session.commit()
        session.refresh(db_user)
        return db_user
    return {"error": "User not found"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return {"message": "User deleted"}
    return {"error": "User not found"}



@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/teas")
def get_teas():
    return teas

@app.post("/teas")
def create_tea(tea: Tea):
    teas.append(tea)
    return tea


app.put("/teas/{tea_id}")
def update_tea(tea_id: int, updated_tea: Tea):
    for i, t in enumerate(teas):
        if t.id == tea_id:
            teas[i] = updated_tea
            return updated_tea
    return {"error": "Tea not found"}


@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    for index, t in enumerate(teas):
        if t.id == tea_id:
            teas.pop(index)
            return {"message": "Tea deleted"}
    return {"error": "Tea not found."}