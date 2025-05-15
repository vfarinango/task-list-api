from flask import abort, make_response
from sqlalchemy import asc, desc
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

def get_models_with_filters(cls, filters=None):
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
    models_response = [model.to_dict() for model in models]

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


