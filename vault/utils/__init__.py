from typing import final
import colander
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

def trycatcher(f):
    def wrapper(self):
        try:
            return f(self)
        except colander.UnsupportedFields as ex:
            self.request.response.status = 400
            return {"err": ex.asdict()[''], "exc": ex.__class__.__name__}
        except colander.Invalid as ex:
            self.request.response.status = 400
            return {"err": ex.asdict(), "exc": ex.__class__.__name__}
        except NoResultFound as ex:
            self.request.response.status = 404
            return {"err": ex, "exc": ex.__class__.__name__}
        except SQLAlchemyError as ex:
            self.request.response.status = 500
            return {"err": ex, "exc": ex.__class__.__name__}
        except Exception as ex:
            self.request.response.status = 500
            return {"err": ex, "exc": ex.__class__.__name__}
    return wrapper

def validate(schema):
    def dec(f):
        def wrapper(self):
            schema.deserialize(self.request.json_body)
            return f(self)
        return wrapper
    return dec