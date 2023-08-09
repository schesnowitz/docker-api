
from pydantic import BaseModel

class PostBaseClass(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateUpdate(PostBaseClass):
    pass

class PostResponse(PostBaseClass):
    title: str
    content: str
    time_created: bool

    class Config:
        from_attributes = True
