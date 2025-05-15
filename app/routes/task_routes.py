from flask import Blueprint, Response, abort, make_response, request
import requests
from datetime import datetime
from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_filters, call_slackbot
from ..db import db

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)


@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)

@bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)

    return task.to_dict() 


@bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    for attribute, value in request_body.items():
        if hasattr(Task, attribute):
            setattr(task, attribute, value)

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("<id>/<completion_status>")
def modify_task_completion_status(id, completion_status):
    task = validate_model(Task, id)

    if completion_status == 'mark_incomplete':
        task.completed_at = None

    elif completion_status == 'mark_complete':
        task.completed_at = datetime.now()
        #Send a slack message to channel (Someone just completed the task <Task.title>)
        call_slackbot(completion_status, task.title)
    else:
        response = {"details": f"Route {completion_status} not recognized"}
        abort(make_response(response,400))

    db.session.commit()
    
    return Response(status=204, mimetype="application/json")
