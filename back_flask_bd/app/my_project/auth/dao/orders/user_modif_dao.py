from back_flask_bd.app.my_project.auth.dao.general_dao import GeneralDao
from back_flask_bd.app.my_project.auth.domain import UserModificationLog

class UserModificationLogDAO(GeneralDao):

    _domain_type = UserModificationLog