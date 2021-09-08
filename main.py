from fastapi import FastAPI, HTTPException, Response, status
from sqlalchemy import create_engine, select, update
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import delete

from schemas import User, UserDel
from sqlalchemy import create_engine, MetaData
from sqlalchemy import text, insert

app = FastAPI()

engine = create_engine("postgresql+psycopg2://test:123456@localhost/flyfund")
meta = MetaData(engine)
table = Table('users', meta,
              Column('id', Integer, primary_key=True),
              Column('email', String, unique=True),
              Column('name', String),
              Column('password', String)
              )
meta.create_all()


@app.get("/user", status_code=200)
def read_all(response: Response):
    engine.connect()
    sql = text("select id, name, email from users")
    user_raws = engine.execute(sql)
    user_list = [{'id': user[0], 'email': user[1], 'name': user[2]} for user in user_raws]
    if len(user_list) > 0:
        return user_list
    raise HTTPException(status_code=404, detail=f"ERROR to get all Users")


@app.get("/user/{user_id}", status_code=200)
def read_user_id(user_id: int, response: Response):
    engine.connect()
    sql = text(f"select id, name, email from users where id='{user_id}'")
    user_row_id = engine.execute(sql)
    db_response = [user for user in user_row_id]
    if len(db_response) != 0:
        return db_response
    raise HTTPException(status_code=404, detail=f"No id: {user_id} in DB")


@app.put("/user/{user_id}", status_code=200)
def update_user(user_id: int, user_entity: User, response: Response):
    engine.connect()
    sql = text(f"update users set name={user_entity.name}, email={user_entity.email} where id={user_id} returning 'success'")
    user_raws = engine.execute(sql)
    if user_raws[0][0] == 'success':
        return {"Msg": f"user {user_entity.email} get all changes"}
    raise HTTPException(status_code=404, detail=f"No id:{user_id} in DB")


@app.post("/user", status_code=201)
def create_user(user_entity: User, response: Response):
    sql = table.insert().values(
        email=user_entity.email,
        name=user_entity.name,
        password=user_entity.password
    )
    conn = engine.connect()
    try:
        conn.execute(sql)
        return f"Email: {user_entity.email} in DB"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to create user: {user_entity.email}")


@app.delete("/user/{user_id}", status_code=200)
def delete_user(user_id: int, user_entity: UserDel, response: Response):
    sql = delete(table).where(table.c.id == user_id)
    conn = engine.connect()
    try:
        conn.execute(sql)
        return f"Email: {user_entity.email} delete from DB"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Can't delete {user_entity.email}")


@app.patch("/user/{user_id}", status_code=200)
def patch_user(user_id: int, response: Response, user_entity: User):
    sql = select(table).where(table.c.id == user_id)
    conn = engine.connect()
    query = conn.execute(sql)
    result = [item for item in query]
    if len(result) != 0:
        bd_id, user_email, user_name, user_password = result[0]

        if user_name != user_entity.name and user_email != user_entity.email and user_password != user_entity.password:
            sql = update(table).where(table.c.id == user_id).values(name=user_entity.name,
                                                                    email=user_email,
                                                                    password=user_entity.password)
            try:
                conn.execute(sql)
                return f"All was modify in DB"
            except Exception:
                raise HTTPException(status_code=500, detail=f"Can't modify email, name, password")

        if user_name != user_entity.name and user_email != user_entity.email:
            sql = update(table).where(table.c.id == user_id).values(name=user_entity.name,
                                                                    email=user_email)
            try:
                conn.execute(sql)
                return f"Name and Email was modify in DB"
            except Exception:
                raise HTTPException(status_code=500, detail=f"Can't modify email, name")

        if user_email != user_entity.email and user_password != user_entity.password:
            sql = update(table).where(table.c.id == user_id).values(email=user_email,
                                                                    password=user_entity.password)
            try:
                conn.execute(sql)
                return f"Password and Email was modify in DB"
            except Exception:
                raise HTTPException(status_code=500, detail=f"Can't modify email, password")

        if user_name != user_entity.name and user_password != user_entity.password:
            sql = update(table).where(table.c.id == user_id).values(name=user_entity.name,
                                                                    password=user_entity.password)
            try:
                conn.execute(sql)
                return f"Name and Password was modify in DB"
            except Exception:
                raise HTTPException(status_code=500, detail=f"Can't modify name, password")

        if user_name != user_entity.name:
            sql = update(table).where(table.c.id == user_id).values(name=user_entity.name)
            try:
                conn.execute(sql)
                return f"Name was modify in DB"
            except Exception:
                raise HTTPException(status_code=500, detail=f"Can't modify name")

        if user_email != user_entity.email:
            sql = update(table).where(table.c.id == user_id).values(email=user_entity.email)
            try:
                conn.execute(sql)
                return f"Email was modify in DB"
            except Exception:
                raise HTTPException(status_code=500, detail=f"Can't modify email")

        if user_password != user_entity.password:
            sql = update(table).where(table.c.id == user_id).values(password=user_entity.password)
            try:
                conn.execute(sql)
                return f"Password was modify in DB"
            except Exception:
                raise HTTPException(status_code=500, detail=f"Can't modify password")
        return f"No need modify"
