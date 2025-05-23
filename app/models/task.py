from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] =  mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="task_ids")

    
    def to_dict(self):
        task_dict = {
            "task": {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete()
            }
        }

        if self.goal_id:
            task_dict["task"]["goal_id"]= self.goal_id

        return task_dict
    
    def is_complete(self):
        return bool(self.completed_at)

    
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            goal_id=task_data.get("goal_id"),
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data["completed_at"]
        )