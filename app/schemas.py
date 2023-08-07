
from pydantic import BaseModel

class PostBaseClass(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreateUpdate(PostBaseClass):
    pass