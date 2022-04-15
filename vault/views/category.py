
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError

from vault.models.category import Category

@view_config(route_name='category', renderer='json')
def category_view(request):
    try:
        categories = request.dbsession.query(Category).all()
    except SQLAlchemyError as ex:
        db_err_msg = ex
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'categories': categories, 'project': 'vault'}
