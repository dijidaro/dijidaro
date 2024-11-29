from flask import render_template
from flask import current_app as app

def init_error_handlers(app):
    # Client Errors (400-499)
    @app.errorhandler(Exception)
    def handle_client_errors(error):
        status_code = getattr(error, 'code', 500)
        if 400 <= int(status_code, 10) <= 499:
            app.logger.warning(f"Client Error {status_code}: {str(error)}")
            return render_template(
                'errors/client_error.html',
                error_code=status_code,
                error_message=str(error)
            ), status_code
        
        elif 500 <= status_code <= 599:
            app.logger.error(f"Server Error {status_code}: {str(error)}")
            return render_template(
                'errors/server_error.html',
                error_code=status_code,
                error_message="Something went wrong on our side. Our team is working to resolve this issue. Please try again later."
            ), status_code
        else:
            app.logger.error(f"Unhandled Error: {str(error)}")
            return render_template(
                'errors/custom_error.html',
                error_message="An unexpected error occurred. Please contact support if this persists."
            ), status_code