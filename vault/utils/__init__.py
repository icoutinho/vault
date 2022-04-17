import colander
from sqlalchemy.exc import SQLAlchemyError
from pyramid.response import Response

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
        except SQLAlchemyError as ex:
            return Response({"err": ex, "exc": ex.__class__.__name__}, content_type='application/json', status=500)
        except Exception as ex:
            return Response({"err": ex, "exc": ex.__class__.__name__}, content_type='application/json', status=500)
    return wrapper

def validate(schema):
    def dec(f):
        def wrapper(self):
            schema.deserialize(self.request.json_body)
            return f(self)
        return wrapper
    return dec