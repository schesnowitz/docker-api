from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
app = FastAPI()
# uvicorn fast.main:app --reload



class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False


@app.post("/blog")
def create(request:Blog):
    return {'payload':f"{request.title}"}



@app.get("/blog")
def index(limit = 20, published:bool = True, sort: Optional[str] = None):
    # http://127.0.0.1:8000/blog?limit=50
    # http://127.0.0.1:8000/blog?limit=50&published=true
    if published:
        return {'payload':f"Blog list of {limit} Published "}
    else:
        return {'payload':f"Blog list of {limit}"}