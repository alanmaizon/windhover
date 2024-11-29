from flask import Blueprint
from svg_paths import SVG_PATHS

# Define the blueprint
base_bp = Blueprint('base', __name__)

@base_bp.app_context_processor
def inject_icons():
    """
    Automatically inject icons into the base.html template context.
    
    """
    return {'ico': SVG_PATHS}
