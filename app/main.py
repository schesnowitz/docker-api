from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

fake_post_data = [{"title": "working with FastApi", "content": "Fast api is cool", "id":1, "published":True},
         {"title": "Get a job", "content": "gotta get a job", "id":2},]

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


@app.get("/")
# async def root():
def root():
    return {'posts': fake_post_data}


@app.get("/posts/")
# async def root():
def get_all_posts():
    return {"data": "This is a post 1"}

 
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
# async def root():
def create_post(post:Post):
    # print(post.rating)
    print(post.model_dump())
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000000)
    fake_post_data.append(post_dict)
    return {"data":post_dict}

""" Validation Long version
@app.get("/posts/{id}")
def get_post(id:int, response: Response): # fastapi converts into into :int
    post =  get_single_post_by_id(int(id)) # no need to convert to int here as argument conversion by fastapi above
    if not post:
        # response.status_code = 404  this is manual way, but import status from fast...
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"message": f"Post with ID:{id} was not found."}
    print(post)
    return{"Post Detail":post}
"""    

@app.get("/posts/{id}")
def get_post(id:int): # fastapi converts into into :int
    post =  get_single_post_by_id(int(id)) # no need to convert to int here as argument conversion by fastapi above
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} was not found.")
    # print(post)
    return{"Post Detail":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int): # fastapi converts into into :int
    post =  delete_single_post_by_id(id) # no need to convert to int here as argument conversion by fastapi above
    index = delete_single_post_by_id(id)
    print(f"index in del {post}")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} was not found.")

    
    fake_post_data.pop(post)


    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_post(id:int, post:Post): # fastapi converts into into :int
#     post =  get_single_post_by_id(int(id)) # no need to convert to int here as argument conversion by fastapi above
    
#     print(post.model_dump())
#     post_dict = post.model_dump()
#     print(post)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} was not found.")
#     # post_dict = post.model_dump_json()
#     # post_dict["id"] == id
#     # fake_post_data[post] == post_dict

    
#     return{"Post Detail":post}


# @app.put("/posts/{id}")
# def update_post(post: Post, id: int):
#     for post in fake_post_data:
#         if post['id'] == id:
#             print(post["title"])
#             if post['title'] is not None:
#                 post['title']  = post['title'] 
#             if post['content'] is not None:
#                 post['content']  = post['content'] 
            
#                 return post['title'] 
#         raise HTTPException(status_code=404, detail=f"Could not find post with id: {id}")
    

@app.put("/posts/{id}")
def update_post(post: Post, id: int):
     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} was not found.")
        index = get_single_post_by_id(id)
        # print(post.model_dump())    
        post_dict = post.model_dump()  
        print(post_dict)
        index =  delete_single_post_by_id(id)
        post_dict['id'] = id
        fake_post_data[index] = post_dict

        print(post_dict)
        return 
