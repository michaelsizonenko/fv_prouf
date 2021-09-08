from sqlalchemy import Column, Integer, String


class User:
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    email = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    password = Column(String, nullable=False)







