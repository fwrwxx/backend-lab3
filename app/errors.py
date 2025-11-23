from flask import jsonify
from flask_jwt_extended import JWTManager

def register_error_handlers(app):
    def not_found(e):
        return {"error": "Not found"}, 404

    def bad_request(e):
        return {"error": "Bad request"}, 400

    def server_error(e):
        return {"error": "Internal server error"}, 500

    app.register_error_handler(404, not_found)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(500, server_error)

    # JWT errors
    @app.errorhandler(422)
    def handle_unprocessable(e):
        return {"error": "Invalid request"}, 422

    from .extensions import jwt

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token(error):
        return jsonify({"message": "Invalid token", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token(error):
        return jsonify({"error": "authorization_required", "description": "Token missing"}), 401
