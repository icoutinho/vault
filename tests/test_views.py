from multiprocessing import dummy
from vault import models
from vault.views.notfound import notfound_view
from vault.views.category import CategoryView
from pytest import fixture
import json



def test_get_category_view_success_filter(dummy_request, dbsession):
    dbsession.add(models.Category(name='games'))
    dbsession.add(models.Category(name='furniture'))
    dbsession.flush()
    dummy_request.params = {"name": "furniture"}
    info = CategoryView(dummy_request).home()
    assert dummy_request.response.status_code == 200
    assert len(info['categories']) == 1
    dummy_request.params = {"name": "games"}
    info = CategoryView(dummy_request).home()
    assert dummy_request.response.status_code == 200
    assert len(info['categories']) == 1
    dummy_request.params = {"name": "books"}
    info = CategoryView(dummy_request).home()
    assert dummy_request.response.status_code == 200
    assert len(info['categories']) == 0
    dummy_request.params = {}
    info = CategoryView(dummy_request).home()
    assert dummy_request.response.status_code == 200
    assert len(info['categories']) == 2

def test_post_category_view_success(dummy_request, dbsession):
    new_category = models.Category(name='books')
    dummy_request.body = json.dumps(new_category)
    print(dummy_request.body)
    dummy_request.method = 'POST'
    assert len(dbsession.query(models.Category).all()) == 0
    info = CategoryView(dummy_request).add()
    assert dummy_request.response.status_code == 200
    assert len(dbsession.query(models.Category).all()) == 1


def test_notfound_view(app_request):
    info = notfound_view(app_request)
    assert app_request.response.status_int == 404
    assert info == {}
