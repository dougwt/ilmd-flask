from ilovemydachshund import app, gallery

url_rules = [
    ('/', gallery.Home.as_view('home')),
    ('/<int:id>/', gallery.Single.as_view('single')),
]

for (rule, func) in url_rules:
    app.add_url_rule(rule, view_func=func)
