from flask import Flask, render_template, g, request, Response, jsonify
import os
from ISRS.model import db
from ISRS.color import colors

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.cfg')

    db.init_app(app)

    @app.route('/')
    def index():
        elements = [("comment" + str(i)) for i in range(30)]
        return render_template('index.html', comments=elements)
    @app.route('/js')
    def js():
        return render_template('index2.html')

    @app.route('/test', methods=['OPTIONS'])
    def test_options():
        print('OPTIONS check')
        res = Response("OK")
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return res

    @app.route('/test', methods=['POST', 'GET'], provide_automatic_options=False)
    def test():
        data = request.get_json()
        print('-'*40, " request.data")
        print(request.data)
        print('-'*40, " content type")
        print(request.content_type)
        print('-'*40, " form")
        print(request.form)
        print('-'*40, " json data")
        print(data)
        print('-'*40, ' get data')
        print(request.get_data())
        print('-'*40, ' jsonify')
        print(jsonify(data))
        print(type(jsonify(data)))
        json_resp = jsonify(data)
        json_resp.headers['Access-Control-Allow-Origin'] = '*'
        return json_resp

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
