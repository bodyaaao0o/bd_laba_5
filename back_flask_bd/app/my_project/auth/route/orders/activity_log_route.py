from http import HTTPStatus
from os import abort

from flask import Blueprint, jsonify, Response, request, make_response

from back_flask_bd.app.my_project import db
from back_flask_bd.app.my_project.auth.controller.orders.activity_log_cantroller import ActivityLogController
from back_flask_bd.app.my_project.auth.domain import ActivityLog
from back_flask_bd.app.my_project.auth.domain.orders import activity_log

activity_log_controller_instance = ActivityLogController()
activity_log_bp = Blueprint('activity_log', __name__, url_prefix='/activity_log')

@activity_log_bp.get('/')
def get_all_activity_logs() -> Response:
    try:
        activity_log_controller_instance = ActivityLogController()
        logs = activity_log_controller_instance.find_all()  # Ensure this method exists
        print("Знайдені записи активності:", logs)
        return make_response(jsonify(logs), HTTPStatus.OK)
    except Exception as e:
        print("Помилка при отриманні записів активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося отримати записи активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@activity_log_bp.post('/')
def create_activity_log() -> Response:
    content = request.get_json()
    if content is None:
        return make_response(jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST)

    try:
        activity_log = ActivityLog.create_from_dto(content)
        db.session.add(activity_log)
        db.session.commit()
        return make_response(jsonify(activity_log.put_into_dto()), HTTPStatus.CREATED)
    except Exception as e:
        print("Помилка при створенні запису активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося створити запис активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@activity_log_bp.get('/<int:user_activity_log_id>')
def get_activity_log(user_activity_log_id: int) -> Response:
    activity_log_controller_instance = ActivityLogController()
    try:
        log = activity_log_controller_instance.find_by_id(user_activity_log_id)  # Ensure this method exists
        return make_response(jsonify(log), HTTPStatus.OK)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND)

@activity_log_bp.put('/<int:user_activity_log_id>')
def update_activity_log(user_activity_log_id: int) -> Response:
    content = request.get_json()
    if content is None:
        return make_response(jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST)

    activity_log_controller_instance = ActivityLogController()
    try:
        activity_log = ActivityLog.create_from_dto(content)
        activity_log_controller_instance.update(user_activity_log_id, activity_log)  # Ensure this method exists
        return make_response("Activity log updated", HTTPStatus.OK)
    except Exception as e:
        print("Помилка при оновленні запису активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося оновити запис активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@activity_log_bp.patch('/<int:user_activity_log_id>')
def patch_activity_log(user_activity_log_id: int) -> Response:
    content = request.get_json()
    if content is None:
        return make_response(jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST)

    activity_log_controller_instance = ActivityLogController()
    try:
        activity_log_controller_instance.patch(user_activity_log_id, content)  # Ensure this method exists
        return make_response("Activity log updated", HTTPStatus.OK)
    except Exception as e:
        print("Помилка при частковому оновленні запису активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося частково оновити запис активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@activity_log_bp.delete('/<int:user_activity_log_id>')
def delete_activity_log(user_activity_log_id: int) -> Response:
    activity_log_controller_instance = ActivityLogController()
    try:
        activity_log_controller_instance.delete(user_activity_log_id)  # Ensure this method exists
        return make_response("Activity log deleted", HTTPStatus.OK)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        print("Помилка при видаленні запису активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося видалити запис активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@activity_log_bp.get('/<int:user_activity_log_id>/user')
def get_users_by_activity_log(user_activity_log_id: int) -> Response:
    try:
        data = activity_log_controller_instance.find_users_by_action(user_activity_log_id)  # Ensure this method exists
        return make_response(jsonify(data), HTTPStatus.OK)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        print("Помилка при отриманні користувачів за записом активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося отримати користувачів за записом активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)