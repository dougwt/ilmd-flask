import gallery

url_rules = [
    ('/', gallery.Home.as_view('home')),
    ('/<id>/', gallery.Single.as_view('single')),
]
