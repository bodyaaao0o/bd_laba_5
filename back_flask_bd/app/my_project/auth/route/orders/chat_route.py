from http import HTTPStatus
from os import abort

from flask import Blueprint, jsonify, Response, request, make_response
from back_flask_bd.app.my_project.auth.controller import chat_controller
from back_flask_bd.app.my_project.auth.domain.orders.chat import Chat

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/', methods=['GET'])
def get_all_chats() -> Response:
    """
    Отримати всі чати
    ---
    tags:
      - Chats
    responses:
      200:
        description: Список всіх чатів
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
                example: "Груповий чат"
              created_at:
                type: string
                format: date-time
    """
    chat_controller_instance = chat_controller()
    return make_response(jsonify(chat_controller_instance.find_all()), HTTPStatus.OK)

@chat_bp.route('/', methods=['POST'])
def create_chat() -> Response:
    """
    Створити новий чат
    ---
    tags:
      - Chats
    parameters:
      - in: body
        name: chat
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            chat_name:
              type: string
              example: "new Name"
    responses:
      201:
        description: Чат успішно створений
      400:
        description: Некоректні дані
    """
    content = request.get_json()

    chat = Chat.create_from_dto(content)

    chat_controller_instance = chat_controller()
    chat_controller_instance.create(chat)

    return make_response(jsonify(chat.put_into_dto()), HTTPStatus.CREATED)

@chat_bp.route('/<int:chat_id>', methods=['GET'])
def get_chat(chat_id: int) -> Response:
    """
    Отримати чат за ID
    ---
    tags:
      - Chats
    parameters:
      - in: path
        name: chat_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Дані чату
      404:
        description: Чат не знайдено
    """
    chat_controller_instance = chat_controller()
    return make_response(jsonify(chat_controller_instance.find_by_id(chat_id)), HTTPStatus.OK)

@chat_bp.route('/<int:chat_id>', methods=['PUT'])
def update_chat(chat_id: int) -> Response:
    """
    Повністю оновити чат
    ---
    tags:
      - Chats
    parameters:
      - in: path
        name: chat_id
        type: integer
        required: true
        example: 1
      - in: body
        name: chat
        required: true
        schema:
          type: object
          properties:
            chat_name:
              type: string
              example: "Updated name"
    responses:
      200:
        description: Чат оновлено
      400:
        description: Некоректні дані
      404:
        description: Чат не знайдено
    """
    content = request.get_json()

    if content is None:
        abort(HTTPStatus.BAD_REQUEST, "No data provided")

    chat = Chat.create_from_dto(content)

    chat_controller_instance = chat_controller()
    chat_controller_instance.update(chat_id, chat)

    return make_response(chat.put_into_dto(),"Chat  updated", HTTPStatus.OK)

@chat_bp.route('/<int:chat_id>', methods=['PATCH'])
def patch_chat(chat_id: int) -> Response:
    """
    Частково оновити чат
    ---
    tags:
      - Chats
    parameters:
      - in: path
        name: chat_id
        type: integer
        required: true
        example: 1
      - in: body
        name: chat_patch
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "New updated name"
    responses:
      200:
        description: Чат оновлено
      404:
        description: Чат не знайдено
    """
    content = request.get_json()
    chat_controller_instance = chat_controller()
    chat_controller_instance.patch(chat_id, content)
    return make_response("Chat updated", HTTPStatus.OK)

@chat_bp.route('/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id: int) -> Response:
    """
    Видалити чат
    ---
    tags:
      - Chats
    parameters:
      - in: path
        name: chat_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Чат видалено
      404:
        description: Чат не знайдено
    """
    chat_controller_instance = chat_controller()
    chat_controller_instance.delete(chat_id)
    return make_response("Chat deleted", HTTPStatus.OK)