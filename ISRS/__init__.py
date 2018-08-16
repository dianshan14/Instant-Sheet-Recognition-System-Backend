from flask import Flask, render_template, g
import os
from ISRS.model import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.cfg')

    db.init_app(app)

    @app.route('/')
    def index():
        elements = [("comment" + str(i)) for i in range(30)]
        return render_template('index.html', comments=elements)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import action
    app.register_blueprint(action.bp)

    #from . import admin
    #app.register_blueprint(admin.bp)

    from . import mobile
    app.register_blueprint(mobile.bp)

    print(app.url_map)

    return app
