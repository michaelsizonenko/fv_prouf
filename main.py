from fastapi import FastAPI, Request, Response, status
from schemas import User

app = FastAPI()

users_list = []

user_id_int = 1


@app.get("/user", status_code=200)
def read_all(response: Response):
    if len(users_list) > 0:
        return {"Users": [key.get('name') for key in users_list]}
    return {"Msg": "No users in DB"}


@app.get("/user/{user_id}", status_code=200)
def read_user_id(user_id: int, response: Response):
    if len(users_list) > 0 and any(u_i == user_id for u_i in [key.get('id') for key in users_list]):
        for user in users_list:
            if user_id == user.get('id'):
                return user
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"Msg": "No users in DB"}


@app.put("/user", status_code=200)
def update_user(user_entity: User, response: Response):
    if user_entity.email in [key.get('email') for key in users_list]:
        for user in users_list:
            if user_entity.email == user['email'] and user_entity.name != user['name'] and user_entity.password != user['password']:
                users_list[users_list.index(user)] = user_entity
                return {"Msg": f"user {user_entity.email} changed Name and Password"}
            if user_entity.email == user['email'] and user_entity.password != user['password']:
                users_list[users_list.index(user)] = user_entity
                return {"Msg": f"user {user_entity.email} changed Password"}
            if user_entity.email == user['email'] and user_entity.name != user['name']:
                users_list[users_list.index(user)] = user_entity
                return {"Msg": f"user {user_entity.email} changed Name"}
            return {"Msg": "No changes"}
    return {"Msg": "User not exist, can't update"}


@app.post("/user", status_code=201)
def create_user(user_entity: User):
    if user_entity.email not in [key.get('email') for key in users_list]:
        user_entity.id = len(users_list) + 1
        users_list.append(dict(user_entity))
        return {"Msg": f"user {user_entity.email} added"}
    return {"Msg": "User exist, try another"}


@app.delete("/user")
def delete_user(user_entity: User):
    if user_entity.email in [key.get('email') for key in users_list]:
        for user in users_list:
            if user_entity.email == user['email']:
                users_list.remove(users_list[users_list.index(user)])
        return {"Msg": f"user {user_entity.email} delete"}
    return {"Msg": "User exist, try another"}
