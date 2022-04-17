from multiprocessing import dummy
from vault import models
from vault.views.notfound import notfound_view
from vault.views.category import CategoryView



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

def test_post_category_view_success(testapp, dbsession):
    new_category = models.Category(name='books')
    assert len(dbsession.query(models.Category).all()) == 0
    info = testapp.post_json('/category.json', new_category.to_dict())
    assert info.status_int == 200
    assert len(dbsession.query(models.Category).all()) == 1
    inserted = dbsession.query(models.Category).first()
    assert 'id' in inserted.__dict__

def test_post_category_invalid(testapp, dbsession):
    new_category = models.Category(name='over32charactersstring_12312391203912391209301293120393210391203912381293812098310928')
    info = testapp.post_json('/category.json', new_category.to_dict(), expect_errors=True)
    assert info.status_int == 400
    assert 'name' in info.json["err"]
    assert info.json["exc"] == "Invalid"
    info = testapp.post_json('/category.json', {}, expect_errors=True)
    assert info.status_int == 400
    assert info.json["err"]['name'] == 'Required'
    assert info.json["exc"] == "Invalid"
    info = testapp.post_json('/category.json', {"name": "books", "theme": "romance"}, expect_errors=True)
    assert info.status_int == 400
    assert 'Unrecognized keys in mapping' in info.json['err']
    assert info.json["exc"] == "UnsupportedFields"
    


def test_notfound_view(app_request):
    info = notfound_view(app_request)
    assert app_request.response.status_int == 404
    assert info == {}
