import os
from flask import Flask

# create_app is APplication Factory function instead of global Flask() instance object
def create_app(test_config=None):
    app = Flask(import_name=__name__,instance_relative_config=True)
    # application configs
    app.config.from_mapping(SECRET_KEY='dev', 
                            DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'))
    
    
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # instance folder will have runtime configurations and databases
    # that should NOT be under version control
    os.makedirs(app.instance_path,exist_ok=True)
    
    @app.route('/hello')
    def hello():
        return "Hello world!!"
    
    # Init DB during startup
    from . import db
    db.init_app(app)

    # Register auth blueprint in auth.py file
    from . import auth
    app.register_blueprint(auth.bp)
    
    # Register blog blueprint from blog.py file
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")
    return app