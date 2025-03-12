import os
import json
import django
from django.apps import apps
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
django.setup()

def get_model_info():
    """
    Collects information about all models in installed Django apps.
    Returns a dictionary suitable for JSON serialization.
    """
    model_data = {}
    
    # Get all installed apps
    for app_config in apps.get_app_configs():
        # Skip Django's built-in apps if you only want your custom apps
        if app_config.name.startswith('django.'):
            continue
        
        # Get all models in the app
        models = list(app_config.get_models())
        
        # Skip apps with no models
        if not models:
            continue
        
        # Process each model in the app
        for model in models:
            model_info = {
                "table_name": model._meta.db_table,
                "description": f"{model.__name__}({', '.join(field.name for field in model._meta.fields)})",
                "fields": {}
            }
            
            # Get all fields in the model
            for field in model._meta.fields:
                field_info = {
                    "type": field.__class__.__name__,
                    "description": field.help_text or f"{field.name} field",
                    "required": not field.null and not field.blank,
                    "default": str(field.default) if field.has_default() else None
                }
                model_info["fields"][field.name] = field_info
            
            # Add the model to the output
            model_data[model.__name__] = model_info
    
    return model_data

def generate_context_json(output_file='rag_context.json'):
    """
    Generates a JSON file with model context for RAG.
    """
    try:
        # Get model information
        context_data = get_model_info()
        
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully generated context file: {output_file}")
        print(f"Found {len(context_data)} models")
        
        # Print summary
        for model_name, model_info in context_data.items():
            print(f"- {model_name}: {len(model_info['fields'])} fields")
            
    except Exception as e:
        print(f"Error generating context file: {str(e)}")

def verify_json_file(file_path='rag_context.json'):
    """
    Verifies the generated JSON file can be loaded correctly.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"JSON file verification successful. Contains {len(data)} models.")
        return True
    except Exception as e:
        print(f"JSON verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Generate the JSON file
    generate_context_json()
    
    # Verify the generated file
    verify_json_file()
