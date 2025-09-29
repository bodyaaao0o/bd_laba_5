from http import HTTPStatus
from os import abort

from flask import Blueprint, jsonify, Response, request, make_response

from back_flask_bd.app.my_project import db
from back_flask_bd.app.my_project.auth.controller.orders.activity_log_cantroller import ActivityLogController
from back_flask_bd.app.my_project.auth.domain import ActivityLog
from back_flask_bd.app.my_project.auth.domain.orders import activity_log

activity_log_controller_instance = ActivityLogController()
activity_log_bp = Blueprint('activity_log', __name__, url_prefix='/activity_log')

@activity_log_bp.route('/', methods=['GET'])
def get_all_activity_logs() -> Response:
    """
    Отримати всі записи активності
    ---
    tags:
      - Activity Logs
    responses:
      200:
        description: Список записів активності
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              user_id:
                type: integer
                example: 1
              action:
                type: string
                example: "LOGIN"
              description:
                type: string
                example: "Користувач увійшов в систему"
              timestamp:
                type: string
                format: date-time
      500:
        description: Помилка сервера
    """
    try:
        activity_log_controller_instance = ActivityLogController()
        logs = activity_log_controller_instance.find_all()
        print("Знайдені записи активності:", logs)
        return make_response(jsonify(logs), HTTPStatus.OK)
    except Exception as e:
        print("Помилка при отриманні записів активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося отримати записи активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@activity_log_bp.route('/', methods=['POST'])
def create_activity_log() -> Response:
    """
    Створити новий запис активності
    ---
    tags:
      - Activity Logs
    parameters:
      - in: body
        name: activity_log
        required: true
        schema:
          type: object
          required:
            - user_id
            - action
          properties:
            user_id:
              type: integer
              example: 1
            action:
              type: string
              example: "LOGIN"
              enum: ["LOGIN", "LOGOUT", "CREATE", "UPDATE", "DELETE", "VIEW"]
            description:
              type: string
              example: "Користувач увійшов в систему"
            ip_address:
              type: string
              example: "192.168.1.100"
    responses:
      201:
        description: Запис активності створений
      400:
        description: Некоректні дані
      500:
        description: Помилка сервера
    """
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

@activity_log_bp.route('/<int:user_activity_log_id>', methods=['GET'])
def get_activity_log(user_activity_log_id: int) -> Response:
    """
    Отримати запис активності за ID
    ---
    tags:
      - Activity Logs
    parameters:
      - in: path
        name: user_activity_log_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Дані запису активності
      404:
        description: Запис не знайдено
    """
    activity_log_controller_instance = ActivityLogController()
    try:
        log = activity_log_controller_instance.find_by_id(user_activity_log_id)
        return make_response(jsonify(log), HTTPStatus.OK)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND)

@activity_log_bp.route('/<int:user_activity_log_id>', methods=['PUT'])
def update_activity_log(user_activity_log_id: int) -> Response:
    """
    Повністю оновити запис активності
    ---
    tags:
      - Activity Logs
    parameters:
      - in: path
        name: user_activity_log_id
        type: integer
        required: true
        example: 1
      - in: body
        name: activity_log
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: integer
              example: 2
            action:
              type: string
              example: "DELETE"
            description:
              type: string
              example: "Оновлений опис"
    responses:
      200:
        description: Запис оновлений
      400:
        description: Некоректні дані
      404:
        description: Запис не знайдено
    """
    content = request.get_json()
    if content is None:
        return make_response(jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST)

    activity_log_controller_instance = ActivityLogController()
    try:
        activity_log = ActivityLog.create_from_dto(content)
        activity_log_controller_instance.update(user_activity_log_id, activity_log)
        return make_response("Activity log updated", HTTPStatus.OK)
    except Exception as e:
        print("Помилка при оновленні запису активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося оновити запис активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@activity_log_bp.route('/<int:user_activity_log_id>', methods=['PATCH'])
def patch_activity_log(user_activity_log_id: int) -> Response:
    """
    Частково оновити запис активності
    ---
    tags:
      - Activity Logs
    parameters:
      - in: path
        name: user_activity_log_id
        type: integer
        required: true
        example: 1
      - in: body
        name: activity_log_patch
        required: true
        schema:
          type: object
          properties:
            description:
              type: string
              example: "Оновлений опис"
            action:
              type: string
              example: "VERIFIED"
    responses:
      200:
        description: Запис оновлений
      404:
        description: Запис не знайдено
    """
    content = request.get_json()
    if content is None:
        return make_response(jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST)

    activity_log_controller_instance = ActivityLogController()
    try:
        activity_log_controller_instance.patch(user_activity_log_id, content)
        return make_response("Activity log updated", HTTPStatus.OK)
    except Exception as e:
        print("Помилка при частковому оновленні запису активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося частково оновити запис активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@activity_log_bp.route('/<int:user_activity_log_id>', methods=['DELETE'])
def delete_activity_log(user_activity_log_id: int) -> Response:
    """
    Видалити запис активності
    ---
    tags:
      - Activity Logs
    parameters:
      - in: path
        name: user_activity_log_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Запис видалений
      404:
        description: Запис не знайдено
    """
    activity_log_controller_instance = ActivityLogController()
    try:
        activity_log_controller_instance.delete(user_activity_log_id)
        return make_response("Activity log deleted", HTTPStatus.OK)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        print("Помилка при видаленні запису активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося видалити запис активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@activity_log_bp.route('/<int:user_activity_log_id>/user', methods=['GET'])
def get_users_by_activity_log(user_activity_log_id: int) -> Response:
    """
    Отримати користувачів за записом активності
    ---
    tags:
      - Activity Logs
    parameters:
      - in: path
        name: user_activity_log_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Користувачі за записом активності
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Іван Іванов"
              email:
                type: string
                example: "ivan@example.com"
      404:
        description: Запис не знайдено
    """
    try:
        data = activity_log_controller_instance.find_users_by_action(user_activity_log_id)
        return make_response(jsonify(data), HTTPStatus.OK)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        print("Помилка при отриманні користувачів за записом активності:", str(e))
        return make_response(jsonify({"error": "Не вдалося отримати користувачів за записом активності"}), HTTPStatus.INTERNAL_SERVER_ERROR)