from flask import Flask
from sqlalchemy.exc import OperationalError

from models import db
from routes.pos import pos as pos_bp
from routes.health import health_bp
import config

def create_app():
    app = Flask(__name__)

    app.config.from_object(config.Config)

    db.init_app(app)
    app.register_blueprint(pos_bp)
    app.register_blueprint(health_bp)

    with app.app_context():
        try:
            db.create_all()
        except OperationalError as e:
            print(f"Database connection error: {e}")
            raise

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
