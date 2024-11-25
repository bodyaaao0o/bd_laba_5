import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from back_flask_bd.app.my_project import db

def insert_into_table(table_name, column_string, value_string):
    query = text(f"INSERT INTO {table_name} ({column_string}) VALUES ({value_string})")

    logging.info(f"Executing query: {query}")

    try:
        with db.engine.connect() as connection:
            with connection.begin():
                connection.execute(query)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}


def call_add_chat_participant(user_name, chat_name):
    query = text(f"CALL AddChatParticipant(:user_name, :chat_name)")

    try:
        with db.engine.connect() as connection:
            with connection.begin():
                connection.execute(query, {'user_name': user_name, 'chat_name': chat_name})
        return {"success": True}
    except Exception as e:
        raise Exception(f"Error executing stored procedure: {str(e)}")




def insert_noname_user_statuses():
    try:
        with db.engine.connect() as connection:
            with connection.begin():
                connection.execute(text("CALL InsertNonameUserStatuses()"))
        return {"success": "Noname user statuses added successfully"}
    except Exception as e:
        return {"error": f"Error inserting user statuses: {str(e)}"}


def call_column_stat(table_name, column_name, operation):
    try:
        query = text("CALL CallColumnStat(:table_name, :column_name, :operation)")
        with db.engine.connect() as connection:
            result = connection.execute(query, {
                "table_name": table_name,
                "column_name": column_name,
                "operation": operation
            }).fetchone()
        return {"result": result[0]} if result else {"error": "No result returned"}
    except Exception as e:
        return {"error": str(e)}


def execute_create_random_tables_and_copy_data():
    connection = None
    try:
        # Отримуємо сирий зв'язок із базою
        connection = db.engine.raw_connection()
        cursor = connection.cursor()

        cursor.callproc('CreateRandomTablesAndCopyData')

        cursor.close()
        connection.commit()  # Фіксуємо зміни
        return {"success": True, "message": "Procedure executed successfully."}
    except Exception as e:
        logging.error(f"Error executing procedure CreateRandomTablesAndCopyData: {str(e)}")
        return {"error": str(e)}
    finally:
        if connection:
            connection.close()


def check_tables_exist():
    result = db.session.execute(text("SHOW TABLES LIKE 'user_data_%'"))
    tables = result.fetchall()

    tables_list = [{"table_name": table[0]} for table in tables]

    if tables_list:
        return {"success": True, "tables": tables_list}
    else:
        return {"error": "No tables found"}




