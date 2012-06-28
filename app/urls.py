from app import app, gallery, login, admin

url_rules = [
    ('/', gallery.Home.as_view('home')),
    ('/<int:id>/', gallery.Single.as_view('single')),
    ('/admin/upload', admin.SubmitImage.as_view('submit-image')),
    ('/login', login.login),
    ('/login/authorized', login.facebook_authorized),
    ('/logout', login.logout),
]

for (rule, func) in url_rules:
    app.add_url_rule(rule, view_func=func)
