from fastapi import FastAPI, Request
from schemas import User

app = FastAPI()

users_list = []


@app.get("/user")
def read_all():
    if len(users_list) > 0:
        return {"Users": [key.get('name') for key in users_list]}
    return {"error": "Don't have any users"}


@app.put("/user")
def update_user(item: User):
    if item.dict()['email'] in [key.get('email') for key in users_list]:
        for user in users_list:
            if item.dict()['email'] == user['email'] and item.dict()['name'] != user['name'] and item.dict()['password'] != user['password']:
                users_list[users_list.index(user)] = item.dict()
                return {"Msg": f"user {item.dict()['email']} changed Name and Password"}
            if item.dict()['email'] == user['email'] and item.dict()['password'] != user['password']:
                users_list[users_list.index(user)] = item.dict()
                return {"Msg": f"user {item.dict()['email']} changed Password"}
            if item.dict()['email'] == user['email'] and item.dict()['name'] != user['name']:
                users_list[users_list.index(user)] = item.dict()
                return {"Msg": f"user {item.dict()['email']} changed Name"}
            return {"Msg": "No changes"}
    return {"Msg": "User not exist, can't update"}


@app.post("/user")
def create_user(item: User):
    if item.dict()['email'] not in [key.get('email') for key in users_list]:
        users_list.append(dict(item))
        return {"Msg": f"user {item.dict()['email']} added"}
    return {"Msg": "User exist, try another"}


@app.delete("/user")
def delete_user(item: User):
    if item.dict()['email'] in [key.get('email') for key in users_list]:
        for user in users_list:
            if item.dict()['email'] == user['email']:
                users_list.remove(users_list[users_list.index(user)])
        return {"Msg": f"user {item.dict()['email']} delete"}
    return {"Msg": "User exist, try another"}


