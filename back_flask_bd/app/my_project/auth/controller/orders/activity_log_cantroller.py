from back_flask_bd.app.my_project.auth.controller.general_controller import GeneralController
from back_flask_bd.app.my_project.auth.service.orders.activity_log_service import ActivityLogService

class ActivityLogController(GeneralController):
    def __init__(self):
        super().__init__(ActivityLogService())

    def find_users_by_action(self, user_activity_log_id: int):
        return ActivityLogService().get_users_by_activity_log(user_activity_log_id)