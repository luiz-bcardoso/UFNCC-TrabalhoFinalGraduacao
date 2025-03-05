import os
import django
import json
from django.apps import apps
from django.db import models

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projeto.settings")
django.setup()

def get_model_schema(app_name):
    app_models = apps.get_app_config(app_name).get_models()
    schema = []

    for model in app_models:
        model_info = {
            "model": model.__name__,
            "fields": [],
            "description": model.__doc__ or "No description provided."
        }

        for field in model._meta.get_fields():
            # Skip reverse relationships
            if field.auto_created:
                continue

            field_info = {
                "name": field.name,
                "type": field.get_internal_type(),
                "description": getattr(field, "help_text", "No description provided.")
            }

            if field.is_relation:
                field_info["related_model"] = field.related_model.__name__
                if field.many_to_many:
                    field_info["relation_type"] = "many_to_many"
                elif field.one_to_one:
                    field_info["relation_type"] = "one_to_one"
                else:
                    field_info["relation_type"] = "foreign_key"

            model_info["fields"].append(field_info)

        schema.append(model_info)

    return schema

def generate_json_for_rag(app_names):
    rag_context = {}

    for app_name in app_names:
        rag_context[app_name] = get_model_schema(app_name)

    with open("django_models_context.json", "w") as f:
        json.dump(rag_context, f, indent=4)

# List of your Django apps
app_names = ["consulta", "fornecedor", "medicamento", "paciente", "triagem", "unidade", "usuario"]

# Generate the JSON file
generate_json_for_rag(app_names)
