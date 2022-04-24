from http.client import REQUEST_TIMEOUT
from pyramid.view import view_config
from pyramid.view import view_defaults
from vault import routes
from vault.models.category import Category, category_schema
from sqlalchemy import and_
from ..utils import trycatcher, validate



@view_defaults(route_name='category')
class CategoryView:
    def __init__(self, request):
        self.request = request
        self.view_name = 'CategoryView'

    @trycatcher
    @view_config(route_name='category_json', request_method='GET', renderer='json')
    @view_config(request_method='GET', renderer='templates/category.jinja2')
    def get_list(self):
        conditions = []
        for key, value in self.request.params.items():
            if value is not None: conditions.append(getattr(Category, key) == value)

        if len(conditions) > 0:
            categories = self.request.dbsession.query(Category).filter(and_(*conditions)).all()
        else:
            categories = self.request.dbsession.query(Category).all()
        return {'categories': categories }

    @trycatcher
    @view_config(route_name='category_one_json', request_method='GET', renderer='json')
    def get_one(self):
        one = self.request.dbsession.query(Category).filter(Category.name == self.request.matchdict.get('name', None)).one()
        return one

    @trycatcher
    @validate(category_schema)
    @view_config(route_name='category_json', request_method='POST', renderer='json')
    def add(self):
        self.request.dbsession.add(Category(**self.request.json_body))
        self.request.dbsession.flush()
        return {}

