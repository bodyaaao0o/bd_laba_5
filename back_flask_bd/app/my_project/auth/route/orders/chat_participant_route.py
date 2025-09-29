from http import HTTPStatus
from flask import Blueprint, jsonify, make_response, request, abort, Response
from back_flask_bd.app.my_project.auth.controller.orders.chat_participant_controler import ChatParticipantController
from back_flask_bd.app.my_project.auth.domain import ChatParticipant

chat_participant_bp = Blueprint('chat_participant', __name__, url_prefix='/chat_participant')

chat_participant_controller_instance = ChatParticipantController()
user_participant_controller_instance = ChatParticipantController()

@chat_participant_bp.route('/', methods=['GET'])
def get_all_chat_participants() -> Response:
    """
    Отримати всіх учасників чатів
    ---
    tags:
      - Chat Participants
    responses:
      200:
        description: Список всіх учасників чатів
        schema:
          type: array
          items:
            type: object
            properties:
              chat_id:
                type: integer
                example: 1
              user_id:
                type: integer
                example: 5
              joined_at:
                type: string
                format: date-time
    """
    return make_response(jsonify(chat_participant_controller_instance.find_all()), HTTPStatus.OK)

@chat_participant_bp.route('/', methods=['POST'])
def create_chat_participant() -> Response:
    """
    Додати учасника до чату
    ---
    tags:
      - Chat Participants
    parameters:
      - in: body
        name: participant
        required: true
        schema:
          type: object
          required:
            - chat_id
            - user_id
          properties:
            chat_id:
              type: integer
              example: 1
            user_id:
              type: integer
              example: 5
    responses:
      201:
        description: Учасник успішно доданий до чату
      400:
        description: Некоректні дані
    """
    content = request.get_json()
    chat_participant = ChatParticipant(**content)
    chat_participant_controller_instance.create(chat_participant)
    return make_response(jsonify(chat_participant.put_into_dto()), HTTPStatus.CREATED)

@chat_participant_bp.route('/chat/<int:chat_id>', methods=['GET'])
def get_chat_participants_by_chat(chat_id: int) -> Response:
    """
    Отримати учасників конкретного чату
    ---
    tags:
      - Chat Participants
    parameters:
      - in: path
        name: chat_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Список учасників чату
      404:
        description: Учасники не знайдені
    """
    participants = chat_participant_controller_instance.get_chat_participants_by_chat(chat_id)
    if not participants:
        return make_response(jsonify({"error": "No participants found for this chat."}), HTTPStatus.NOT_FOUND)
    return make_response(jsonify(participants), HTTPStatus.OK)

@chat_participant_bp.route('/user/<int:user_id>', methods=['GET'])
def get_chat_participants_by_user(user_id: int) -> Response:
    """
    Отримати чати користувача
    ---
    tags:
      - Chat Participants
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        example: 5
    responses:
      200:
        description: Список чатів користувача
      404:
        description: Чати не знайдені
    """
    participants = user_participant_controller_instance.get_chat_participants_by_user(user_id)
    if not participants:
        return make_response(jsonify({"error": "No participants found for this chat."}), HTTPStatus.NOT_FOUND)
    return make_response(jsonify(participants), HTTPStatus.OK)

@chat_participant_bp.route('/<int:chat_id>/<int:user_id>', methods=['DELETE'])
def delete_chat_participant(chat_id: int, user_id: int) -> Response:
    """
    Видалити учасника з чату
    ---
    tags:
      - Chat Participants
    parameters:
      - in: path
        name: chat_id
        type: integer
        required: true
        example: 1
      - in: path
        name: user_id
        type: integer
        required: true
        example: 5
    responses:
      204:
        description: Учасник видалений з чату
      404:
        description: Учасник не знайдений
      500:
        description: Помилка сервера
    """
    try:
        chat_participant_controller_instance.delete(chat_id, user_id)
        return make_response(jsonify({"message": "Chat participant deleted successfully."}), HTTPStatus.NO_CONTENT)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND)
    except Exception as e:
        return make_response(jsonify({"error": "An error occurred while deleting the chat participant."}), HTTPStatus.INTERNAL_SERVER_ERROR)