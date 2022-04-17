from sqlalchemy import (
    Column,
    Index,
    Integer,
    String
)
from colanderalchemy import SQLAlchemySchemaNode

from .meta import Base


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=32), nullable=False)


Index('uq_cat_name', Category.name, unique=True, mysql_length=255)
category_schema = SQLAlchemySchemaNode(Category, unknown='raise')