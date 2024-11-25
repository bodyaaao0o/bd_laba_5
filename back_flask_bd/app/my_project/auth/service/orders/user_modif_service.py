from typing import Dict, Any

from back_flask_bd.app.my_project.auth.dao.orders.user_modif_dao import UserModificationLogDAO
from back_flask_bd.app.my_project.auth.service.general_service import GeneralService

class UserModificationLogService(GeneralService):
    def __init__(self):
        super().__init__(UserModificationLogDAO())