from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db 
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# get_db()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None




# connected = False
# while connected == False:
#     try:
#         conn = psycopg2.connect(host="containers-us-west-70.railway.app", 
#                             database="railway", 
#                             user="postgres", 
#                             password="HlpSP7uPQLai4gq0TNnA",  
#                             port="6484", 
#                             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected To Postgres!")
#         connected = True
#     except Exception as e:
#         print(f"Connection failed with this error ->: {e} Trying again in 3 seconds...")
#         time.sleep(3)


  
        




@app.get("/alchemytest")
# async def root():
def alchemytest(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {'payload': posts}


@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts} 

 
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_post(post:Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data":new_post}



@app.get("/posts/{id}")
def get_post(id:int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} was not found.")
    
    return{"Post Detail":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)): 

    post = db.query(models.Post).filter(models.Post.id==id)
    # print(post.id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} was not found.")

    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}")
def update_post(post: Post, id:int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Post with ID:{id} was not found.")
    
    post_query.update({"title":post.title, "content":post.content})
    print(post_query.title)
    db.commit()
 
    return post_query.first
