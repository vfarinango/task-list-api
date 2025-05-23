from flask import abort, make_response, jsonify
from sqlalchemy import asc, desc
from app.models.task import Task
import requests
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        invalid = {"details": f"{cls.__name__} id {model_id} is invalid."}
        abort(make_response(invalid,400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        not_found = {"details": f"{cls.__name__} with id {model_id} was not found."}
        abort(make_response(not_found, 404))

    return model

    

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as e:
        response = {"details": "Invalid data"}
        abort(make_response(response,400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None, to_dict_options=None):
    query = db.select(cls)
    order_by_clause = cls.id

    if filters:
        for parameter, value in filters.items():
            if parameter == "sort":
                if value == "asc":
                    order_by_clause = asc("title")
                elif value == "desc":
                    order_by_clause = desc("title")
            elif hasattr(cls, parameter):
                query = query.where(getattr(cls,parameter).ilike(f"%{value}%"))
    
    models = db.session.scalars(query.order_by(order_by_clause))

    
    models_response = []
    to_dict_options = to_dict_options if to_dict_options is not None else {}
    for model in models:
        model_dict = model.to_dict(**to_dict_options)
        inner_key = cls.__name__.lower()

        if inner_key in model_dict:
            models_response.append(model_dict[inner_key])
        else:
            models_response.append(model_dict)

    return models_response

def call_slackbot(task_title):
    url = "https://hooks.slack.com/services/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"
    text = f"Someone just completed the task: {task_title}"

    try:
        response = requests.post(url=url,json={"text": text},timeout=5.0)
        response.raise_for_status()
    except Exception:
        response = f"An unexpected error occured."
        abort(make_response(response,400))



def validate_task_ids(request_body):
    try:
        if not request_body:
            response = {"details": "Request body is empty."}
            abort(make_response(jsonify(response), 400))
        
        task_ids_from_request = request_body["task_ids"]

        if not isinstance(task_ids_from_request, list):
            response = {"details": "'task_ids' must be a list."}
            abort(make_response(jsonify(response), 400))
        
        for task_id in task_ids_from_request:
            if not isinstance(task_id, int):
                response = {"details": f"Each task ID must be an integer, but received {task_id}."}
                abort(make_response(jsonify(response), 400))
        
        return task_ids_from_request
    
    except KeyError:
        response = {"details": "Request body must contain 'task_ids'."}
        abort(make_response(jsonify(response), 400))
    except Exception as e:
        response = {"details": f"An unexpected error occured: {e}."}
        abort(make_response(jsonify(response), 400))


def get_tasks_from_ids(task_ids_list):
    task_models = []

    for task_id in task_ids_list:
        task_instance =  validate_model(Task, task_id)
        task_models.append(task_instance)
    return task_models
    