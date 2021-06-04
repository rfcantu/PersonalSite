import os

from flask import Flask

def create_app(test_config=None):
    #create and configure
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        TEMPLATES_AUTO_RELOAD = True,
    )

    if test_config is None:
        # load instance since not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # testing, load config is passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Connection test
    @app.route('/test_connect')
    def test_connect():
        return 'Connected to app'
    
    from . import db
    db.init_app(app)

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    from . import tabs_auth
    app.register_blueprint(tabs_auth.bp)

    from . import tab
    app.register_blueprint(tab.bp)

    from . import chords
    app.register_blueprint(chords.bp)

    return app