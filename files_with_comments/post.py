# This file defines Pydantic models for posts and comments.
# These models are used for request validation and response serialization in FastAPI endpoints.

from pydantic import BaseModel, ConfigDict

# Model for incoming post data from the user (request body)
class UserPostIn(BaseModel):
    body: str

# Model for a post as stored/retrieved, includes an ID.
class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True) # Allows ORM mode for SQLAlchemy
    id: int  # Unique identifier for the post

# Model for incoming comment data from the user (request body)
class CommentIn(BaseModel):
    body: str      # The content of the comment
    post_id: int   # The ID of the post this comment belongs to


# Model for a comment as stored/retrieved, includes an ID.
class Comment(CommentIn):
    model_config = ConfigDict(from_attributes=True)  # Allows ORM mode for SQLAlchemy
    id: int  # Unique identifier for the comment


# Model for returning a post along with its comments.
class UserPostWithComments(BaseModel):
    post: UserPost           # The post object
    comments: list[Comment]  # List of comments associated with the post
