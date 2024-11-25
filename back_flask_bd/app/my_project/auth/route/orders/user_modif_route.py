from http import HTTPStatus
from os import abort

from flask import Blueprint, jsonify, Response, request, make_response

from back_flask_bd.app.my_project.auth.controller.orders.user_modif_controller import UserModificationLogController

user_modif_bp =  Blueprint('user_modif', __name__, url_prefix='/user_modif')

@user_modif_bp.route('/', methods=['GET'])
def get_all_users() -> Response:
    user_controller_instance = UserModificationLogController()
    return make_response(jsonify(user_controller_instance.find_all()), HTTPStatus.OK)