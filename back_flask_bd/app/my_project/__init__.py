import os
from typing import Dict, Any
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import inspect
from sqlalchemy_utils import database_exists, create_database
from flasgger import Swagger

from back_flask_bd.app.my_project.auth.route import register_routes
from back_flask_bd.app.my_project.database import db
from back_flask_bd.app.my_project.auth.route.orders.user_route import user_bp
from back_flask_bd.app.my_project.auth.route.orders.user_status_route import user_status_bp

# Імпортуємо функції для роботи з AWS Secrets Manager
try:
    from back_flask_bd.app.my_project.secrets_manager import get_secret, is_aws_environment

    AWS_SECRETS_AVAILABLE = True
except ImportError as e:
    AWS_SECRETS_AVAILABLE = False
    print(f"Warning: AWS Secrets Manager module not available: {e}")

SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
MYSQL_ROOT_USER = "MYSQL_ROOT_USER"
MYSQL_ROOT_PASSWORD = "MYSQL_ROOT_PASSWORD"


def create_app(config_data: Dict[str, Any] = None, additional_config: Dict[str, Any] = None) -> Flask:
    app = Flask(__name__)

    register_routes(app)

    # Перевіряємо чи потрібно використовувати AWS Secrets Manager
    use_aws_secrets = os.getenv('USE_AWS_SECRETS', 'false').lower() == 'true'

    print(f"USE_AWS_SECRETS: {use_aws_secrets}")
    print(f"AWS_SECRETS_AVAILABLE: {AWS_SECRETS_AVAILABLE}")

    if use_aws_secrets and AWS_SECRETS_AVAILABLE:
        print("=" * 60)
        print("Loading configuration from AWS Secrets Manager...")
        print("=" * 60)
        try:
            secrets = get_secret()

            # Конфігурація бази даних з AWS Secrets
            db_host = secrets.get('DB_HOST', '').replace('https://', '').replace('http://', '')
            db_port = secrets.get('DB_PORT', '3306')
            db_user = secrets.get('DB_USER')
            db_pass = secrets.get('DB_PASS')
            db_name = secrets.get('DB_NAME')

            print(f"DB_HOST: {db_host}")
            print(f"DB_PORT: {db_port}")
            print(f"DB_USER: {db_user}")
            print(f"DB_NAME: {db_name}")

            # Формуємо DATABASE_URI
            app.config['SQLALCHEMY_DATABASE_URI'] = (
                f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
            )

            # Flask конфігурація
            app.config['SECRET_KEY'] = secrets.get('SECRET_KEY')
            app.config['DEBUG'] = secrets.get('FLASK_ENV') == 'development'

            print("=" * 60)
            print("✓ Successfully loaded configuration from AWS Secrets Manager")
            print("=" * 60)

        except Exception as e:
            print("=" * 60)
            print(f"✗ Error loading secrets from AWS: {e}")
            print("Falling back to local configuration...")
            print("=" * 60)
            use_aws_secrets = False

    # Якщо не використовуємо AWS або сталася помилка, використовуємо локальну конфігурацію
    if not use_aws_secrets:
        print("=" * 60)
        print("Using local YAML configuration")
        print("=" * 60)

        if config_data:
            app.config.update(config_data)
        if additional_config:
            _process_input_config(app.config, additional_config)

        app.config.setdefault(
            'SQLALCHEMY_DATABASE_URI', 'mysql://root:password@localhost/newww'
        )
        app.config.setdefault('SECRET_KEY', os.urandom(24))

    # Загальні налаштування
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    migrate = Migrate(app, db)
    db.init_app(app)
    Swagger(app)

    with app.app_context():
        try:
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✓ Підключення до БД успішне!")
            print(f"✓ Список таблиць у базі даних: {tables}")
        except Exception as e:
            print(f"✗ Помилка підключення до бази даних: {e}")
            print(
                f"Database URI (без пароля): {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set').split(':')[0]}://...")

    return app


def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    root_user = additional_config.get(MYSQL_ROOT_USER)
    root_password = additional_config.get(MYSQL_ROOT_PASSWORD)

    if root_user and root_password:
        if SQLALCHEMY_DATABASE_URI in app_config:
            app_config[SQLALCHEMY_DATABASE_URI] = app_config[SQLALCHEMY_DATABASE_URI].format(
                root_user=root_user, root_password=root_password
            )
    else:
        raise ValueError("MYSQL_ROOT_USER and MYSQL_ROOT_PASSWORD must be provided in additional_config.")


def _init_db(app: Flask) -> None:
    db.init_app(app)
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    if db_uri and not database_exists(db_uri):
        create_database(db_uri)
    import back_flask_bd.app.my_project.auth.domain
    with app.app_context():
        db.create_all()