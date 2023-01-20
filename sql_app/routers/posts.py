from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models,schema, Oauth2
from ..database import get_db
from datetime import datetime
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


#* Get all the Posts fromt the database
@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(Oauth2.get_current_user), limit: int = 10):

    print(limit)
    posts = db.query(models.Posts).filter(models.Posts.user_id == current_user.id).order_by(models.Posts.dateCreated.desc()).all()
    return posts




#* Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post:schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    new_post = models.Posts(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    




#* get the specific posts according to the ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    fetch_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    print(fetch_post)
    
    if fetch_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find the post")

    return fetch_post


#* Delete the Posts
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    
    index = db.query(models.Posts).filter(models.Posts.id == id)

    post = index.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content Does Not Exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="FORBIDDEN! Unauthorized Access.")


    index.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

#* Update the Posts
@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED, response_model=schema.Post)
def update_post(id:int, post:schema.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    

    updated_post = db.query(models.Posts).filter(models.Posts.id == id)

    upost = updated_post.first()

    if upost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content Not found")
     
    updated_post.update(post.dict(), synchronize_session=False)

    db.commit()
    return upost

















    # #* Testing the database Connection
# try:
#     #* create the connection to the db
#     conn = psycopg2.connect(host='localhost', database='API_DB', user='postgres', password='pande', cursor_factory=RealDictCursor)
#     cur = conn.cursor()                 #* create the cursor
#     print("Connection Succesfull")
# except Exception as err:
#     print("Connection Failed: ",err)



# #* Base Routee for the api
# @router.get("/")
# def read_root():
#     return {"message":"This is the Root Page"}

# #* get all the posts
# @router.get("/posts")
# def get_posts():
#     cur.execute('SELECT * FROM public."Posts"')
#     my_posts = cur.fetchall()
#     return {
#         "data": my_posts
#     }


# #* Create a new post
# @router.post("/create", status_code=status.HTTP_201_CREATED)
# def create_post(new_post: Post):
#     cur.execute('INSERT INTO public."Posts" (title, content, published) VALUES (%s, %s, %s) Returning *', (new_post.title, new_post.content, new_post.published))
#     conn.commit()
#     created_post = cur.fetchone()
#     return {
#         "data": created_post
#     }

# #* get the specific posts according to the ID
# @router.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     cur.execute(f'SELECT * FROM public."Posts" WHERE id = {id}')
#     fetch_post = cur.fetchone()
#     if fetch_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot find the post")
    
#     return {
#         "Post Details": fetch_post
#     }

# #* Delete the Posts
# @router.get("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     cur.execute('DELETE FROM public."Posts" WHERE id = %s Returning *', (str(id),))
#     index = cur.fetchone()
#     conn.commit()

#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content Does Not Exist")

#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#     return {
#         "message": "Post Deleted"
#     }


# #* Update the Posts
# @router.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
# def update_post(id:int, post:Post):
#     cur.execute('UPDATE public."Posts" SET title = %s, content = %s, published=%s WHERE id = %s Returning * ',(post.title, post.content, post.published, str(id)))
#     updated_post = cur.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content Not found")
     
#     return {
#         "data": updated_post
#     }



