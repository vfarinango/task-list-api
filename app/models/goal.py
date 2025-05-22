from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    task_ids: Mapped[list["Task"]] = relationship(back_populates="goal")
    
    def to_dict(self):
        return {
            "goal": {
                "id": self.id,
                "title": self.title
            }
        }
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title=goal_data["title"],
            task_ids=goal_data.get("task_id", [])
        )
