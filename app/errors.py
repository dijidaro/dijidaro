from flask import render_template
import logging

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 400
    
    @app.errorhandler(500)
    def server_error(error):
        logging.error(f"Internal server: {str(error)}")
        return render_template("errors/500.html"), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(f"An unexpected error occurred: {str(e)}")
        return render_template("errors/500.html"), 500
    