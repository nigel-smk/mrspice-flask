from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    web_id = Column(String)

    def __repr__(self):
        return "<Recipe(web_id='{web_id}')>".format(web_id=self.web_id)


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Ingredient(name='{name}')>".format(name=self.name)