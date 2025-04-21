from fastapi import APIRouter, HTTPException

from mediaapp.models.post import UserPost, UserPostIn, Comment, CommentIn

router = APIRouter()

post_table = {}
comment_table = {}

def find_post(post_id: int):
    return post_table.get(post_id)


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = {**data, "id": last_record_id}
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())

@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    data = comment.model_dump()
    last_record_id = len(comment_table)
    new_comment= {**data, "id": last_record_id}
    comment_table[last_record_id] = new_comment
    return new_comment
