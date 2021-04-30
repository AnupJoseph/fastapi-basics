from typing import Dict, List
from fastapi import FastAPI
from enum import Enum

app: FastAPI = FastAPI()

fake_items_db: List[Dict[str, str]] = [
    {"item_name": "Red"},
    {"item_name": "Shelley"},
    {"item_name": "Vasquez"},
    {"item_name": "Delphi"},
]


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello world"}


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10) -> List[Dict[str, str]]:
    return fake_items_db[skip:skip+limit]


@app.get("/items/{item_id}")
async def return_items(item_id: int) -> Dict[str, int]:
    return {"Item": item_id}
