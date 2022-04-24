def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('healthcheck', '/')
    config.add_route('category', '/category')
    config.add_route('category_json', '/category.json')
    config.add_route('category_one_json', '/category/{name}.json')
