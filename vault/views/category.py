from pyramid.view import view_config
from pyramid.response import Response
from pyramid.view import view_defaults
from sqlalchemy.exc import SQLAlchemyError
from vault.models.category import Category
from sqlalchemy import and_


@view_defaults(route_name='category')
class CategoryView:
    def __init__(self, request):
        self.request = request
        self.view_name = 'CategoryView'

    @view_config(route_name='category_json', request_method='GET', renderer='json')
    @view_config(request_method='GET', renderer='templates/category.jinja2')
    def home(self):
        try:
            conditions = []
            for key, value in self.request.params.items():
                if value is not None: conditions.append(getattr(Category, key) == value)

            if len(conditions):
                categories = self.request.dbsession.query(Category).filter(and_(*conditions)).all()
            else:
                categories = self.request.dbsession.query(Category).all()
        except SQLAlchemyError as ex:
            db_err_msg = ex
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'categories': categories }

    @view_config(route_name='category_json', request_method='POST', renderer='json')
    def add(self):
        try:
            self.request.dbsession.add(Category(**self.request.json_body))
            self.request.dbsession.flush()
        except SQLAlchemyError as ex:
            db_err_msg = ex
            return Response(db_err_msg, content_type='text/plain', status=500)

