from fastapi import FastAPI, HTTPException, Response, status
from schemas import User

app = FastAPI()

user_db = {}


@app.get("/user", status_code=200)
def read_all(response: Response):
    user_list = []
    if len(user_db) > 0:
        for key in user_db:
            user_list.append({'email': user_db[key]['email'], 'name': user_db[key]['name']})
        return user_list
    raise HTTPException(status_code=404, detail="No users in DB")


@app.get("/user/{user_id}", status_code=200)
def read_user_id(user_id: int, response: Response):
    if user_id in user_db:
        return user_db[user_id]
    raise HTTPException(status_code=404, detail=f"No id:{user_id} in DB")


@app.put("/user/{user_id}", status_code=200)
def update_user(user_id: int, user_entity: User, response: Response):
    if user_id in user_db:
        user_entity.id = user_id
        user_db[user_id] = dict(user_entity)
        return {"Msg": f"user {user_entity.email} get all changes"}
    raise HTTPException(status_code=404, detail=f"No id:{user_id} in DB")


@app.post("/user", status_code=201)
def create_user(user_entity: User, response: Response):
    if user_entity.email not in [user_db[key].get('email') for key in user_db]:
        user_entity.id = len(user_db) + 1
        user_db[user_entity.id] = dict(user_entity)
        return {"Msg": f"user {user_entity.email} added"}
    raise HTTPException(status_code=400, detail=f"User {user_entity.email} in DB")


@app.delete("/user/{user_id}", status_code=200)
def delete_user(user_id: int, user_entity: User, response: Response):
    if user_id in user_db:
        del user_db[user_id]
        return {"Msg": f"user {user_entity.email} delete"}
    raise HTTPException(status_code=404, detail=f"No id:{user_id} in DB")


@app.patch("/user/{user_id}", status_code=200)
def patch_user(user_id: int, response: Response, user_entity: User):
    if user_id in user_db:
        existed_user = user_db[user_id]
        if existed_user['name'] != user_entity.name and existed_user['password'] != user_entity.password:
            user_entity.id = user_id
            user_db[user_id] = dict(user_entity)
            return {"Msg": f"user {user_entity.email} changed Name and Password"}
        if existed_user['password'] != user_entity.password:
            user_entity.id = user_id
            user_db[user_id] = dict(user_entity)
            return {"Msg": f"user {user_entity.email} changed Password"}
        if existed_user['name'] != user_entity.name:
            user_entity.id = user_id
            user_db[user_id] = dict(user_entity)
            return {"Msg": f"user {user_entity.email} changed Name"}
        return {"Msg": "No changes"}
    raise HTTPException(status_code=404, detail=f"No id:{user_id} in DB")
