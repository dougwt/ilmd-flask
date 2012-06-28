from app import app, gallery, login

url_rules = [
    ('/', gallery.Home.as_view('home')),
    ('/<int:id>/', gallery.Single.as_view('single')),
    ('/login', login.login),
    ('/login/authorized', login.facebook_authorized),
    ('/logout', login.logout),
]

for (rule, func) in url_rules:
    app.add_url_rule(rule, view_func=func)
