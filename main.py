from typing import Annotated
from fastapi import FastAPI, Body, Path, status, HTTPException

app = FastAPI(
    title="My First Project",
    summary="My CRUD application.",
    version="0.0.1",
    openapi_tags=[{"name": "users", "description": "User operations"}]
)

comments_db = {0: "First comment in FastAPI"}

@app.get("/comments", tags=["users"])
async def read_comments() -> dict:
    return comments_db

@app.get("/comments/{comment_id}", tags=["users"])
async def read_comment(comment_id: Annotated[int, Path(ge=0, title="Comment ID")]) -> str:
    if comment_id in comments_db:
        return comments_db[comment_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

@app.post("/comments", tags=["users"], status_code=status.HTTP_201_CREATED)
async def create_comment(text: str = Body(...)) -> str:
    current_index = max(comments_db) + 1 if comments_db else 0
    comments_db[current_index] = text
    return "Comment created!"

@app.put("/comments/{comment_id}", tags=["users"])
async def update_comment(comment_id: Annotated[int, Path(ge=0, title="Comment ID")], 
                         text: str = Body(...)) -> str:
    if comment_id in comments_db:
        comments_db[comment_id] = text
        return "Comment updated!"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

@app.delete("/comments/{comment_id}", tags=["users"])
async def delete_comment(comment_id: Annotated[int, Path(ge=0, title="Comment ID")]) -> str:
    if comment_id in comments_db:
        comments_db.pop(comment_id)
        return "Comment deleted!"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
