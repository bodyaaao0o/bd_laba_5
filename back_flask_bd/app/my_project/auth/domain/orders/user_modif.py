from __future__ import annotations
from datetime import datetime
from back_flask_bd.app.my_project.database import db
from back_flask_bd.app.my_project.auth.domain.i_dto import IDto

class UserModificationLog(db.Model, IDto):
    __tablename__ = 'user_modification_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    old_email = db.Column(db.String(100), nullable=True)
    old_user_name = db.Column(db.String(50), nullable=True)
    new_email = db.Column(db.String(100), nullable=True)
    new_user_name = db.Column(db.String(50), nullable=True)
    modification_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return (
            f"UserModificationLog(id={self.id}, user_id={self.user_id}, "
            f"old_email={self.old_email}, old_user_name={self.old_user_name}, "
            f"new_email={self.new_email}, new_user_name={self.new_user_name}, "
            f"modification_time={self.modification_time})"
        )

    def put_into_dto(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'old_email': self.old_email,
            'old_user_name': self.old_user_name,
            'new_email': self.new_email,
            'new_user_name': self.new_user_name,
            'modification_time': self.modification_time
        }

    @staticmethod
    def create_from_dto(dto: dict) -> UserModificationLog:
        return UserModificationLog(**dto)
