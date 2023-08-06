from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

fake_post_data = [{"title": "working with FastApi", "content": "Fast api is cool", "id":1, "published":True},
         {"title": "Get a job", "content": "gotta get a job", "id":2},]


connected = False
while connected == False:
    try:
        conn = psycopg2.connect(host="containers-us-west-70.railway.app", 
                            database="railway", 
                            user="postgres", 
                            password="HlpSP7uPQLai4gq0TNnA",  
                            port="6484", 
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected To Postgres!")
        connected = True
    except Exception as e:
        print(f"Connection failed with this error ->: {e} Trying again in 3 seconds...")
        time.sleep(3)



def get_single_post_by_id(id):
    for post in fake_post_data:
        if id == post['id']:
            return post    
        

def delete_single_post_by_id(id):
    for index, post in enumerate(fake_post_data):
        if post['id'] == id:
            print(index)
            return index 
app = FastAPI()
# uvicorn main:app --reload


# @app.get("/")
# # async def root():
# def root():
#     return {'posts': fake_post_data}


@app.get("/posts")
def get_all_posts():

    cursor.execute(""" SELECT * FROM posts """)  
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts} 

 
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_post(post:Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)RETURNING * """, 
                   (post.title, post.content, post.published))
    conn.commit()
    new_post = cursor.fetchone()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id:int): # fastapi converts into into :int
    cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} was not found.")
    # print(post)
    return{"Post Detail":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int): # fastapi converts into into :int
    cursor.execute(""" DELETE from posts WHERE id = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} was not found.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}")
def update_post(post: Post, id: int):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                      (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Post with ID:{id} was not found.")
 

    
    return post
