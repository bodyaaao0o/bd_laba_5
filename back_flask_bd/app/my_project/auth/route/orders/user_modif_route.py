from http import HTTPStatus
from os import abort

from flask import Blueprint, jsonify, Response, request, make_response

from back_flask_bd.app.my_project.auth.controller.orders.user_modif_controller import UserModificationLogController

user_modif_bp = Blueprint('user_modif', __name__, url_prefix='/user_modif')

@user_modif_bp.route('/', methods=['GET'])
def get_all_users() -> Response:
    """
    Отримати всі записи модифікацій користувачів
    ---
    tags:
      - User Modifications
    responses:
      200:
        description: Список всіх записів модифікацій користувачів
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
                example: 5
              modification_type:
                type: string
                example: "UPDATE"
              old_values:
                type: string
                example: "name: 'Old Name', email: 'old@example.com'"
              new_values:
                type: string
                example: "name: 'New Name', email: 'new@example.com'"
              modified_at:
                type: string
                format: date-time
                example: "2024-01-15T10:30:00Z"
      500:
        description: Помилка сервера
    """
    user_controller_instance = UserModificationLogController()
    return make_response(jsonify(user_controller_instance.find_all()), HTTPStatus.OK)