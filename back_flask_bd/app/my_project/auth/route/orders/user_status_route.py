from http import HTTPStatus
from os import abort

from flask import Blueprint, jsonify, Response, request, make_response

from back_flask_bd.app.my_project import db
from back_flask_bd.app.my_project.auth.controller import user_status_controller
from back_flask_bd.app.my_project.auth.controller.orders.user_status_controller import UserStatusController
from back_flask_bd.app.my_project.auth.domain import UserStatus

user_status_bp = Blueprint('user_status', __name__, url_prefix='/user_status')

# @user_status_bp.route('/', methods=['GET'])
# def get_all_user_status() -> Response:
#     """
#     Отримати всі статуси користувачів
#     ---
#     tags:
#       - User Status
#     responses:
#       200:
#         description: Список всіх статусів
#         schema:
#           type: array
#           items:
#             type: object
#             properties:
#               id:
#                 type: integer
#                 example: 1
#               status:
#                 type: string
#                 example: "Active"
#       500:
#         description: Помилка сервера
#     """
#     try:
#         user_status_controller_instance = UserStatusController()
#         statuses = user_status_controller_instance.find_all()
#         print("Знайдені статуси:", statuses)
#         return make_response(jsonify(statuses), HTTPStatus.OK)
#     except Exception as e:
#         print("Помилка при отриманні статусів:", str(e))
#         return make_response(jsonify({"error": "Не вдалося отримати статуси"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@user_status_bp.route('/', methods=['POST'])
def create_user_status() -> Response:
    """
    Створити новий статус користувача
    ---
    tags:
      - User Status
    parameters:
      - in: body
        name: status
        required: true
        schema:
          type: object
          required:
            - status_name
          properties:
            status:
              type: string
              example: "Premium"
    responses:
      201:
        description: Статус створений
      400:
        description: Некоректні дані
    """
    content = request.get_json()
    user_status = UserStatus.create_from_dto(content)
    db.session.add(user_status)
    db.session.commit()
    return make_response(jsonify(user_status.put_into_dto()), HTTPStatus.CREATED)

@user_status_bp.route('/<int:user_status_id>', methods=['GET'])
def get_user_status(user_status_id: int) -> Response:
    """
    Отримати статус за ID
    ---
    tags:
      - User Status
    parameters:
      - in: path
        name: status_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Дані статусу
      404:
        description: Статус не знайдено
    """
    user_status_controller_instance = UserStatusController()
    return make_response(jsonify(user_status_controller_instance.find_by_id(user_status_id)), HTTPStatus.OK)

@user_status_bp.route('/<int:user_status_id>', methods=['PUT'])
def update_user_status(user_status_id: int) -> Response:
    """
    Повністю оновити статус
    ---
    tags:
      - User Status
    parameters:
      - in: path
        name: status_id
        type: integer
        required: true
        example: 1
      - in: body
        name: status
        required: true
        schema:
          type: object
          properties:
            status_name:
              type: string
              example: "Updated Status"
    responses:
      200:
        description: Статус оновлений
      400:
        description: Некоректні дані
      404:
        description: Статус не знайдено
    """
    content = request.get_json()
    if content is None:
        abort(HTTPStatus.BAD_REQUEST, "No data provided")
    user_status = UserStatus.create_from_dto(content)
    user_status_controller_instance = UserStatusController()
    user_status_controller_instance.update(user_status_id, user_status)
    return make_response("User status updated", HTTPStatus.OK)

@user_status_bp.route('/<int:user_status_id>', methods=['PATCH'])
def patch_user_status(user_status_id: int) -> Response:
    """
    Частково оновити статус
    ---
    tags:
      - User Status
    parameters:
      - in: path
        name: status_id
        type: integer
        required: true
        example: 1
      - in: body
        name: status_patch
        required: true
        schema:
          type: object
          properties:
            status:
              type: string
              example: "New Name"
    responses:
      200:
        description: Статус оновлений
      404:
        description: Статус не знайдено
    """
    content = request.get_json()
    user_status_controller_instance = UserStatusController()
    user_status_controller_instance.patch(user_status_id, content)
    return make_response("User status updated", HTTPStatus.OK)

@user_status_bp.route('/<int:user_status_id>', methods=['DELETE'])
def delete_user_status(user_status_id: int) -> Response:
    """
    Видалити статус
    ---
    tags:
      - User Status
    parameters:
      - in: path
        name: status_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Статус видалений
      404:
        description: Статус не знайдено
    """
    user_status_controller_instance = UserStatusController()
    user_status_controller_instance.delete(user_status_id)
    return make_response("User status deleted", HTTPStatus.OK)

@user_status_bp.route('/<int:user_status_id>/user', methods=['GET'])
def get_users_by_status(user_status_id: int) -> Response:
    """
    Отримати користувачів за статусом
    ---
    tags:
      - User Status
    parameters:
      - in: path
        name: user_status_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Список користувачів з цим статусом
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              user_name:
                type: string
                example: "II-100-10"
              email:
                type: string
                example: "email@gmail.com"
              password:
                type: string
                example: "password"
              user_status_id:
                type: integer
                example: 1
              status:
                 type: string
                 example: "Online"
      404:
        description: Статус не знайдено або користувачі відсутні
    """
    user_status_controller_instance = UserStatusController()
    try:
        data = user_status_controller_instance.find_users_by_status(user_status_id)
        return make_response(jsonify(data), HTTPStatus.OK)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND)