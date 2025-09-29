from typing import Dict, Any, List

from back_flask_bd.app.my_project.auth.dao import activity_log_dao
from back_flask_bd.app.my_project.auth.dao.orders.user_dao import UserDAO
from back_flask_bd.app.my_project.auth.dao.orders.activity_log_dao import ActivityLogDao
from back_flask_bd.app.my_project.auth.service.general_service import GeneralService

class ActivityLogService(GeneralService):
    def __init__(self):
        super().__init__(ActivityLogDao())

    def get_users_by_activity_log(self, user_activity_log_id: int) -> Dict[str, Any]:
        activity_log_dao = ActivityLogDao()
        user_action = activity_log_dao.find_by_id(user_activity_log_id)
        if not user_action:
            raise ValueError("User status not found.")

        users = [user.put_into_dto() for user in UserDAO().get_users_by_action(user_activity_log_id)]
        return {
            "user_status": user_action.put_into_dto(),
            "users": users
        }