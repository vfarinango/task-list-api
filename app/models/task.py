from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    
    def to_dict(self):
        return {
            "task": {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }
        }
    
    def is_complete(self):
        return bool(self.completed_at)

    
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data["completed_at"]
        )