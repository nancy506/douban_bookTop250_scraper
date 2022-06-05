import os

from flask import Flask
import sqlite3 as sql
from flask import render_template

from douban import ingestor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'
    
    from . import ingestor
    ingestor.init_app(app)
    
    @app.route('/list')
    def list():
        cur = ingestor.get_db().execute("select * from books")        
        rows = cur.fetchall()
        return render_template("list.html",rows = rows)
    
    @app.route('/index')
    def index():
        return render_template("index.html",)

    return app

app = Flask(__name__)

@app.route("/")
#def hello_world():
    #return "<p>Hello, Wdsdsdsorld!</p>"

def hello(name=None):
    return render_template('index.html', name=name)

if __name__ == '__main__':
   app.run()