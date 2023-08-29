from flask import Flask
from app.views import database_blueprint
app = Flask(__name__)
app.register_blueprint(database_blueprint)

if __name__ == "__main__":
    app.run()
