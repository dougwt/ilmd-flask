from flask import Flask
from urls import url_rules
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)

for (rule, func) in url_rules:
    app.add_url_rule(rule, view_func=func)

if __name__ == '__main__':
    app.debug = True
    app.run()
