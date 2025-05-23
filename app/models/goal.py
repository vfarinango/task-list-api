from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")
    
    def to_dict(self, with_tasks=False):
        goal_dict = {
            "goal": {
                "id": self.id,
                "title": self.title
            }
        }

        if with_tasks:
            goal_dict["tasks"] = [task.to_dict()["task"] for task in self.tasks]
        
        return goal_dict
    
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title=goal_data["title"]
        )
