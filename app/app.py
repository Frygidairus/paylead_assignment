from flask import Flask
import logging
from sqlalchemy.exc import OperationalError
import time

from models import db
from routes.pos import pos as pos_bp
from routes.health import health_bp
import config

logging.basicConfig(
    level=logging.INFO,  # Show INFO and above
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    app.config.from_object(config.Config)

    db.init_app(app)
    app.register_blueprint(pos_bp)
    app.register_blueprint(health_bp)

    with app.app_context():
        retries = 5
        while retries > 0:
            try:
                db.create_all()
                logger.info("Database ready")
                break
            except OperationalError as e:
                retries -= 1
                logger.warning(f"Database connection error: {e}")
                logger.warning(f"Retrying... ({5 - retries}/5)")
                time.sleep(2)
        else:
            raise RuntimeError("Could not connect to the database after several retries.")


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
