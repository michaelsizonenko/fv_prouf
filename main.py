from fastapi import FastAPI, Request, Response, status
from schemas import User

app = FastAPI()

user_db = {}


@app.get("/user", status_code=200)
def read_all(response: Response):
    if len(user_db) > 0:
        return {user_db[key].get('name') for key in user_db}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Msg": "No users in DB"}


@app.get("/user/{user_id}", status_code=200)
def read_user_id(user_id: int, response: Response):
    if user_id in user_db:
        return user_db[user_id]
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Msg": "No users in DB"}


@app.put("/user/{user_id}", status_code=200)
def update_user(user_id: int, user_entity: User, response: Response):
    if user_id in user_db:
        user_entity.id = user_id
        user_db[user_id] = dict(user_entity)
        return {"Msg": f"user {user_entity.email} get all changes"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Msg": "User not exist, can't update"}


@app.post("/user", status_code=201)
def create_user(user_entity: User, response: Response):
    if user_entity.email not in [user_db[key].get('email') for key in user_db]:
        user_entity.id = len(user_db) + 1
        user_db[user_entity.id] = dict(user_entity)
        return {"Msg": f"user {user_entity.email} added"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Msg": "User exist, try another"}


@app.delete("/user/{user_id}", status_code=200)
def delete_user(user_id: int, user_entity: User, response: Response):
    if user_id in user_db:
        del user_db[user_id]
        return {"Msg": f"user {user_entity.email} delete"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Msg": "User exist, try another"}


@app.patch("/user/{user_id}", status_code=200)
def patch_user(user_id: int, response: Response, user_entity: User):
    if user_id in user_db:
        if user_db[user_id]['name'] != user_entity.name and user_db[user_id]['password'] != user_entity.password:
            user_entity.id = user_id
            user_db[user_id] = dict(user_entity)
            return {"Msg": f"user {user_entity.email} changed Name and Password"}
        if user_db[user_id]['password'] != user_entity.password:
            user_entity.id = user_id
            user_db[user_id] = dict(user_entity)
            return {"Msg": f"user {user_entity.email} changed Password"}
        if user_db[user_id]['name'] != user_entity.name:
            user_entity.id = user_id
            user_db[user_id] = dict(user_entity)
            return {"Msg": f"user {user_entity.email} changed Name"}
        return {"Msg": "No changes"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Msg": "Wrong id"}
