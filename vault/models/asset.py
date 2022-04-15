from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class Asset(Base):
    __tablename__ = 'asset'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


Index('uq_ass_name', Asset.name, unique=True, mysql_length=255)
