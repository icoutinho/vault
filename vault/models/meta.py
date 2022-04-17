from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: https://alembic.sqlalchemy.org/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)

class MyBase(object):
    def __json__(self, request):
        return self.to_dict()

    def to_dict(self):
        json_exclude = getattr(self, '__json_exclude__', set())
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_') and k not in json_exclude}

Base = declarative_base(cls=MyBase, metadata=metadata)
