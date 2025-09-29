from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from waitress.trigger import trigger
from sqlalchemy.sql import text

from back_flask_bd.app.my_project import db
from back_flask_bd.app.my_project.auth.controller.orders.procedure_controller import insert_into_table, \
    insert_noname_user_statuses, call_column_stat, execute_create_random_tables_and_copy_data, check_tables_exist
from back_flask_bd.app.my_project.auth.controller.orders.procedure_controller import call_add_chat_participant
import logging

procedure_bp = Blueprint('procedure_bp', __name__)
trigger_bp = Blueprint('trigger_bp', __name__)
stats_bp = Blueprint('stats_bp', __name__)
logging.basicConfig(level=logging.INFO)

@procedure_bp.route('/insert', methods=['POST'])
def insert_user_data():
    """
    Вставити дані в таблицю
    ---
    tags:
      - Procedures
    parameters:
      - in: body
        name: data
        required: true
        schema:
          type: object
          required:
            - table_name
            - column_string
            - value_string
          properties:
            table_name:
              type: string
              example: "user"
            column_string:
              type: string
              example: "user_name, email"
            value_string:
              type: string
              example: "'John Doe', 'john@example.com'"
    responses:
      200:
        description: Дані успішно вставлені
      400:
        description: Відсутні обов'язкові поля
      500:
        description: Помилка вставки
    """
    data = request.get_json()
    if 'table_name' not in data or 'column_string' not in data or 'value_string' not in data:
        return jsonify({"error": "Missing required fields: 'table_name', 'column_string', or 'value_string'"}), 400

    table_name = data['table_name']
    column_string = data['column_string']
    value_string = data['value_string']
    try:
        result = insert_into_table(table_name, column_string, value_string)
        if 'error' in result:
            return jsonify(result), 500
    except Exception as e:
        logging.error(f"Error inserting data into {table_name}: {e}")
        return jsonify({"error": "An error occurred while inserting data."}), 500
    return jsonify(result), 200

@procedure_bp.route('/add_participant', methods=['POST'])
def add_chat_participant():
    """
    Додати учасника до чату
    ---
    tags:
      - Procedures
    parameters:
      - in: body
        name: data
        required: true
        schema:
          type: object
          required:
            - user_name
            - chat_name
          properties:
            user_name:
              type: string
              example: "John Doe"
            chat_name:
              type: string
              example: "General Chat"
    responses:
      200:
        description: Учасник доданий до чату
      400:
        description: Відсутні обов'язкові поля
      500:
        description: Помилка додавання
    """
    data = request.get_json()

    if 'user_name' not in data or 'chat_name' not in data:
        return jsonify({"error": "Missing required fields: 'user_name' or 'chat_name'"}), 400

    user_name = data['user_name']
    chat_name = data['chat_name']

    try:
        result = call_add_chat_participant(user_name, chat_name)
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error adding participant: {e}")
        return jsonify({"error": str(e)}), 500

@procedure_bp.route('/insert_noname', methods=['POST'])
def insert_noname_users_route():
    """
    Вставити користувачів без імені
    ---
    tags:
      - Procedures
    responses:
      200:
        description: Користувачі без імені додані
      500:
        description: Помилка вставки
    """
    try:
        result = insert_noname_user_statuses()
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error inserting Noname users: {str(e)}")
        return jsonify({"error": str(e)}), 500

@stats_bp.route('/get_column_stat', methods=['POST'])
def get_column_stat():
    """
    Отримати статистику по колонці
    ---
    tags:
      - Statistics
    parameters:
      - in: body
        name: data
        required: true
        schema:
          type: object
          required:
            - table_name
            - column_name
            - operation
          properties:
            table_name:
              type: string
              example: "user"
            column_name:
              type: string
              example: "age"
            operation:
              type: string
              example: "AVG"
              enum: ["COUNT", "SUM", "AVG", "MIN", "MAX"]
    responses:
      200:
        description: Статистика отримана
      400:
        description: Відсутні обов'язкові поля
      500:
        description: Помилка отримання статистики
    """
    try:
        data = request.get_json()
        if not all(key in data for key in ['table_name', 'column_name', 'operation']):
            return jsonify({"error": "Missing required fields: 'table_name', 'column_name', 'operation'"}), 400

        table_name = data['table_name']
        column_name = data['column_name']
        operation = data['operation']

        result = call_column_stat(table_name, column_name, operation)
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error calling column stat procedure: {e}")
        return jsonify({"error": str(e)}), 500

@procedure_bp.route('/create_random_tables', methods=['POST'])
def create_random_tables_and_copy_data_route():
    """
    Створити випадкові таблиці та скопіювати дані
    ---
    tags:
      - Procedures
    responses:
      200:
        description: Таблиці створені та дані скопійовані
      500:
        description: Помилка створення таблиць
    """
    result = execute_create_random_tables_and_copy_data()
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200

@procedure_bp.route('/check_tables', methods=['GET'])
def check_tables_route():
    """
    Перевірити існування таблиць
    ---
    tags:
      - Procedures
    responses:
      200:
        description: Інформація про таблиці
      404:
        description: Таблиці не знайдені
    """
    result = check_tables_exist()
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@trigger_bp.route('/delete_chat/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    """
    Видалити чат (тригер)
    ---
    tags:
      - Triggers
    parameters:
      - in: path
        name: chat_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Чат видалено
      400:
        description: Помилка видалення
    """
    try:
        query = text("DELETE FROM chat WHERE id = :chat_id")
        db.session.execute(query, {"chat_id": chat_id})
        db.session.commit()
        return jsonify({"message": "Chat deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete chat: {str(e)}"}), 400

@trigger_bp.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Оновити користувача (тригер)
    ---
    tags:
      - Triggers
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        example: 1
      - in: body
        name: data
        required: true
        schema:
          type: object
          required:
            - user_name
          properties:
            user_name:
              type: string
              example: "New Name"
    responses:
      200:
        description: Користувач оновлений
      400:
        description: Відсутні дані або помилка
      500:
        description: Помилка сервера
    """
    data = request.json
    user_name = data.get("user_name")
    if not user_name:
        return jsonify({"error": "Missing required field: user_name"}), 400

    try:
        query = text("UPDATE user SET user_name = :user_name WHERE id = :user_id")
        db.session.execute(query, {"user_name": user_name, "user_id": user_id})
        db.session.commit()
        return jsonify({"message": f"User with ID {user_id} updated successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update user: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error occurred: {str(e)}"}), 500

@trigger_bp.route('/insert_user', methods=['POST'])
def insert_user():
    """
    Вставити користувача (тригер)
    ---
    tags:
      - Triggers
    parameters:
      - in: body
        name: data
        required: true
        schema:
          type: object
          required:
            - user_name
          properties:
            user_name:
              type: string
              example: "John Smith"
    responses:
      201:
        description: Користувач вставлений
      400:
        description: Відсутні дані або помилка
    """
    data = request.json
    if "user_name" not in data:
        return jsonify({"error": "Missing required field: user_name"}), 400

    try:
        query = text("INSERT INTO user (user_name) VALUES (:user_name)")
        db.session.execute(query, {"user_name": data["user_name"]})
        db.session.commit()
        return jsonify({"message": "User inserted successfully"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to insert user: {str(e)}"}), 400