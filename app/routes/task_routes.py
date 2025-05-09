from flask import Blueprint, Response, abort, make_response, request
from app.models.task import Task
from .route_utilities import validate_model, create_model
from ..db import db

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)


@bp.get("")
def get_all_tasks():
    pass

@bp.get("/<id>")
def get_one_task(id):
    pass

@bp.put("/<id>")
def update_task(id):
    pass

@bp.delete("/<id>")
def delete_task(id):
    pass