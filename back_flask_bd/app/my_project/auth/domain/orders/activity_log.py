from __future__ import annotations
from datetime import datetime
from back_flask_bd.app.my_project.database import db
from back_flask_bd.app.my_project.auth.domain.i_dto import IDto


class ActivityLog(db.Model, IDto):
    __tablename__ = "activity_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"ActivityLog('{self.id}', '{self.action}', '{self.timestamp}')"

    def put_into_dto(self):
        return {
            'id': self.id,
            'action': self.action,
            'timestamp': self.timestamp
        }

    @staticmethod
    def create_from_dto(dto: dict):
        return ActivityLog(**dto)

