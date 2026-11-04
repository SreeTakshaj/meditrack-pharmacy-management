from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Initialize extensions here so all files can import them
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()