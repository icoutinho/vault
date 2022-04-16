from pyramid.view import view_config
from pyramid.response import Response
from pyramid.view import view_defaults
from sqlalchemy.exc import SQLAlchemyError
from vault.models.category import Category


@view_defaults(route_name='category')
class CategoryView:
    def __init__(self, request):
        self.request = request
        self.view_name = 'CategoryView'

    @view_config(renderer='templates/category.jinja2')
    def home(self):
        try:
            categories = self.request.dbsession.query(Category).all()
        except SQLAlchemyError as ex:
            db_err_msg = ex
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'categories': categories}
