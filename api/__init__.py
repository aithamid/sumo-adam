from flask import Flask
from api.config.development import config


def create_api():
    api = Flask(__name__)

    # Load the appropriate configuration
    api.config.from_object(config)

    # Register blueprints
    from api.routes.cars import cars_bp
    from api.routes.edits import edits_bp
    from api.routes.launchs import launchs_bp

    api.register_blueprint(cars_bp)
    api.register_blueprint(edits_bp)
    api.register_blueprint(launchs_bp)

    return api


api = create_api()

if __name__ == '__main__':
    api.run()
