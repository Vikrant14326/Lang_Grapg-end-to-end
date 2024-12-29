from fastapi import FastAPI,Query,Depends
from typing import Optional,List
from pydantic import BaseModel
from database import Base,engine,SessionLocal

from database import Column,String,Integer,Boolean
app=FastAPI()
class User(Base):
    __tablename__="user"
    id=Coloumn(Integer,primary_key=True,index=True)
    email=Coloumn(String,unique=True,index=True)
    is_active=Coloumn(Boolean,default=True)
    
Base.metadata.create_all(bind=engine)   
# class User(BaseModel):
#     name:str
#     Password:str 
#     address:Optional[str]=None
    
       

# @app.get("/virat")
# def index():
#     return "hellow world"


# @app.get("/item/{item_id}")
# def index(item_id:int):
#     return {"product_id":item_id}

# @app.get("/item/")
# def index(q:int=0,m:Optional[int]=82):
#     return {"product is":q,"m":m}

# # file_path

# @app.get("/items/{file_path:path}")
# def index(file_path:str):
#     return {"file_path": file_path}

# # @app.post("/items")
# # def index(user:User):
# #     return user
#     # return "hello world"

# @app.post("/items/{user_id}")
# def index(user_id:int,user:User):
#     return user
# # query parameters

# @app.get("/items")
# def index(q:Optional[str]=Query(None,min_length=2,max_length=5,regex="^vit")):
    # return {"Q":q}

######################### Dependency Injection ######

# async def common_param(q:Optional[str] = None, skip:int = 0, limit:int = 10):
#     return {"q":q, "skip":skip, "limit":limit}

# @app.get("/items")
# async def read_item(commons:dict = Depends(common_param)):
#     return commons

# @app.get("/users")
# async def get_user(commons: dict = Depends(common_param)):
#     return commons

########################## Dependancy in class ##########

# class CommanPrams:
#     def __init__(self,q:Optional[str]=10,skip:skip=0,limit:limit=0)
#         self.q=q
#         self.skip=skip
#         self.limit=limit  
        
        
        
        
        
        