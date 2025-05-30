from flask import Blueprint, Response, request, jsonify
import requests
from app.models.goal import Goal
from .route_utilities import validate_model, create_model, get_models_with_filters, get_validated_tasks_from_request_body
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal,request.args)

@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return goal.to_dict()


@bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    for attribute, value in request_body.items():
        if hasattr(Goal, attribute):
            setattr(goal, attribute, value)

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

@bp.post("/<id>/tasks")
def add_tasks_to_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    
    tasks_to_add = get_validated_tasks_from_request_body(request_body)
    goal.tasks = tasks_to_add
    
    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": [task.id for task in tasks_to_add]
    }

    return jsonify(response), 200

@bp.get("/<id>/tasks")
def get_tasks_of_one_goal(id):
    goal = validate_model(Goal, id)

    tasks_response_list = []
    for task in goal.tasks:
        tasks_response_list.append(task.to_dict()["task"])

    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response_list
    }
    
    return jsonify(response_body), 200
    


