from vault.views.notfound import notfound_view

def test_my_view_success(testapp):
    res = testapp.get('/', status=200)
    assert res.body

def test_notfound(testapp):
    res = testapp.get('/badurl', status=404)
    assert res.status_code == 404

def test_notfound_view(app_request):
    info = notfound_view(app_request)
    assert app_request.response.status_int == 404
    assert info == {}
