import os
import json
import django
from django.apps import apps
from django.conf import settings

# Set up Django environment
# Replace 'your_project_name' with your actual Django project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
django.setup()

def get_app_info():
    """
    Collects information about all installed Django apps and their models
    Returns a dictionary suitable for JSON serialization
    """
    app_data = {}
    
    # Get all installed apps
    for app_config in apps.get_app_configs():
        # Skip Django's built-in apps if you only want your custom apps
        if app_config.name.startswith('django.'):
            continue
            
        app_info = {
            'name': app_config.name,
            'verbose_name': app_config.verbose_name,
            'description': getattr(app_config, 'description', f"{app_config.verbose_name} application"),
            'models': {}
        }
        
        # Get all models in the app
        for model in app_config.get_models():
            model_info = {
                'name': model.__name__,
                'description': getattr(model, '__doc__', f"Model for {model.__name__}").strip() or f"Model for {model.__name__}",
                'fields': {}
            }
            
            # Get all fields in the model
            for field in model._meta.fields:
                field_info = {
                    'type': field.__class__.__name__,
                    'description': field.help_text or f"{field.name} field",
                    'required': not field.null and not field.blank,
                    'default': str(field.default) if field.has_default() else None
                }
                model_info['fields'][field.name] = field_info
            
            app_info['models'][model.__name__] = model_info
        
        app_data[app_config.name] = app_info
    
    return app_data

def generate_context_json(output_file='rag_context.json'):
    """
    Generates a JSON file with app context for RAG
    """
    try:
        # Get app information
        context_data = get_app_info()
        
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully generated context file: {output_file}")
        print(f"Found {len(context_data)} custom apps")
        
        # Print summary
        for app_name, app_info in context_data.items():
            print(f"- {app_name}: {len(app_info['models'])} models")
            
    except Exception as e:
        print(f"Error generating context file: {str(e)}")

def verify_json_file(file_path='rag_context.json'):
    """
    Verifies the generated JSON file can be loaded correctly
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"JSON file verification successful. Contains {len(data)} apps.")
        return True
    except Exception as e:
        print(f"JSON verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Generate the JSON file
    generate_context_json()
    
    # Verify the generated file
    verify_json_file()