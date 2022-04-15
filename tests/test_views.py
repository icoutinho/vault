from vault import models
from vault.views.default import my_view
from vault.views.notfound import notfound_view
from vault.views.category import category_view
import json


def test_category_view_success(app_request, dbsession):
    dbsession.add(models.Category(name='games'))
    dbsession.add(models.Category(name='furniture'))
    dbsession.flush()
    info = category_view(app_request)
    assert app_request.response.status_code == 200
    assert len(info['categories']) == 2

def test_notfound_view(app_request):
    info = notfound_view(app_request)
    assert app_request.response.status_int == 404
    assert info == {}
