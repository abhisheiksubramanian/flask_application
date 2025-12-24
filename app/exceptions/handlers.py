from flask import jsonify
from app.exceptions.business import BusinessException

def register_error_handlers(app):
    @app.errorhandler(BusinessException)
    def handle_business(e):
        return jsonify(error=str(e)), 400
