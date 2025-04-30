from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI()

class Tea(BaseModel):
    id: int
    name: str
    origin: str
    
    
teas: List[Tea] = []


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