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