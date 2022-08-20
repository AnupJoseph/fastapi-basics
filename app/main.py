# Standard lib
from random import randrange

# External
from rich import print

# FastAPI
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str = "Redwoods in California"
    content: str = "Redwoods in California are tall"


my_posts = [
    {"id": 0, "title": "Zeroth post", "content": "Content of zeroth post"},
    {
        "id": 999,
        "title": "Another post",
        "content": "Content of post after zeroth post",
    },
]


def find_post(id: int):
    return list(filter(lambda x: x.get("id") == id, my_posts))[0]


def find_and_remove_post(id: int):
    try:
        post = find_post(id)
        index = my_posts.index(post)
        my_posts.pop(index)
        print("Post removed from the database")
        return True
    except IndexError:
        print(f"Post with id {id} not present in the database")
        return


@app.get("/")
async def root():
    return {"messsage": "root"}


@app.get("/posts")
async def get_posts():
    """Returns all posts present in the database

    Returns:
        Dict: Dictionary of posts
    """
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    """Create post

    Args:
        post: Post {"title": "Redwoods in California","content":"Redwoods in California are tall"}

    Returns:
        Dict: Created post
    """
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000000)
    print(f"{post_dict=}")
    my_posts.append(post_dict)
    return {"new_post": post_dict}


@app.get("/posts/{id}")
async def get_posts(id: int):
    """Get a specfic post from db

    Args:
        id (int): Id fof the requested post

    Raises:
        HTTPException: Raised when post is not present in the Database

    Returns:
        Dict: The requested post
    """
    try:
        post = find_post(id)
    except IndexError:
        print("Post not present in the database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"post with {id=} not found in the database"},
        )
    return {"post_detail": f"This here be the post you wanted {id} {post}"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int):
    status_ret = find_and_remove_post(id)
    if status_ret:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    elif status_ret is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"post with {id=} not found in the database"},
        )


@app.put("/posts/{id}")
async def update_posts(id: int, post: Post):
    found_post = find_post(id=id)
    index = my_posts.index(found_post)
    print(f"{post=}")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    print(f"{my_posts=}")

    return {"message": post_dict}
