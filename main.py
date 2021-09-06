from fastapi import FastAPI, Request, Response, status
from schemas import User

app = FastAPI()

users_list = {}


@app.get("/user", status_code=200)
def read_all(response: Response):
    if len(users_list) > 0:
        return {users_list[key].get('name') for key in users_list}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Msg": "No users in DB"}


@app.get("/user/{user_id}", status_code=200)
def read_user_id(user_id: int, response: Response):
    if user_id in users_list:
        return users_list[user_id]
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Msg": "No users in DB"}


@app.put("/user/{user_id}", status_code=200)
def update_user(user_id: int, user_entity: User, response: Response):
    if user_id in users_list:
        user_entity.id = user_id
        users_list[user_id] = dict(user_entity)
        return {"Msg": f"user {user_entity.email} get all changes"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Msg": "User not exist, can't update"}


@app.post("/user", status_code=201)
def create_user(user_entity: User, response: Response):
    if user_entity.email not in [users_list[key].get('email') for key in users_list]:
        user_entity.id = len(users_list) + 1
        users_list[user_entity.id] = dict(user_entity)
        return {"Msg": f"user {user_entity.email} added"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Msg": "User exist, try another"}


@app.delete("/user/{user_id}", status_code=200)
def delete_user(user_id: int, user_entity: User, response: Response):
    if user_id in users_list:
        del users_list[user_id]
        return {"Msg": f"user {user_entity.email} delete"}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"Msg": "User exist, try another"}


@app.patch("/user/{user_id}", status_code=200)
def patch_user(user_id: int, response: Response, user_entity: User):
    if user_id in users_list:
        if users_list[user_id]['name'] != user_entity.name and users_list[user_id]['password'] != user_entity.password:
            user_entity.id = user_id
            users_list[user_id] = dict(user_entity)
            return {"Msg": f"user {user_entity.email} changed Name and Password"}
        if users_list[user_id]['password'] != user_entity.password:
            user_entity.id = user_id
            users_list[user_id] = dict(user_entity)
            return {"Msg": f"user {user_entity.email} changed Password"}
        if users_list[user_id]['name'] != user_entity.name:
            user_entity.id = user_id
            users_list[user_id] = dict(user_entity)
            return {"Msg": f"user {user_entity.email} changed Name"}
        return {"Msg": "No changes"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Msg": "Wrong id"}
