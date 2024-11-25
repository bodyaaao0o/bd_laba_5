from back_flask_bd.app.my_project.auth.controller.general_controller import GeneralController
from back_flask_bd.app.my_project.auth.service.orders.user_modif_service import UserModificationLogService

class UserModificationLogController(GeneralController):

    def __init__(self):
        super().__init__(UserModificationLogService())