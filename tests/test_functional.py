from vault import models

def test_my_view_success(testapp):
    res = testapp.get('/', status=200)
    assert res.body

def test_category_success(testapp):
    res = testapp.get('/category', status=200)
    assert res.body

def test_notfound(testapp):
    res = testapp.get('/badurl', status=404)
    assert res.status_code == 404
