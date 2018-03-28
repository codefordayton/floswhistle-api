from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()

