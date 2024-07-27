from flask import Flask

def create_website():
    app = Flask(__name__)

    from website.views import views

    app.register_blueprint(views)

    return app