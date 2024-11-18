from flask import Blueprint
from svg_paths import SVG_PATHS  # Assuming SVG_PATHS is where your paths are stored

# Define the blueprint
base_bp = Blueprint('base', __name__)

@base_bp.app_context_processor
def inject_icons():
    """
    Automatically inject icons into the base.html template context.
    
    """
    print(SVG_PATHS)
    return {'ico': SVG_PATHS}  # Pass icons to all templates