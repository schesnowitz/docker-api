from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import schemas

from . import models
from . database import engine, get_db
from sqlalchemy.orm import Session
app = FastAPI()
# uvicorn fast.main:app --reload

models.Base.metadata.create_all(engine)

@app.post("/blogs", status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, content=request.content)
    db.add(new_blog)
    
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blogs")
def index(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blogs/{id}")
def show(id:int, response:Response, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, the object with the ID:{id} was not found.")
    return blog

@app.put("/blogs/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request:schemas.Blog, db:Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog =  blog.first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, the object with the ID:{id} was not found.")
    # blog.update(request, synchronize_session=False)
    blog.title = request.title
    blog.content = request.content
    
    db.commit()
    return blog

@app.delete("/blogs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, the object with the ID:{id} was not found.")
    blog.delete(synchronize_session=False)
    db.commit() 

