from back_flask_bd.app.my_project.auth.dao.general_dao import GeneralDao
from back_flask_bd.app.my_project.auth.domain import ActivityLog


class ActivityLogDao(GeneralDao):
    _domain_type = ActivityLog
