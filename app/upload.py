from flask import Blueprint, current_app, render_template, flash, abort
from forms import UploadForm
from werkzeug.utils import secure_filename
import os
from auth import login_required
import pymupdf
from io import BytesIO

bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=("GET", "POST"))
@login_required
def upload_resource():
    ## TO DO
    # 1. Grab form data
    # 2. Check if file is indeed pdf. i.e use pdf signatures
    # 3. Check if file contents matches the grabbed form data
    # 4. Save the resource data to a database and the file to a file server storage.
    # 5. Redirect to a success page.
    
    form = UploadForm()
    if form.validate_on_submit():
        error = None
        file = form.uploaded_resource.data
        if file:
            try:
                resource = pymupdf.Document(stream=BytesIO(file.read()), filetype="pdf")
            except OSError as oe:
                abort(400, f"Server only accepts Buffer streams {oe}")
        
        if error is None:
            resource_text = resource[0].get_text().strip()
            # filename = secure_filename(f"{form.school.data.upper()}_{form.subject.data.upper()}_{form.resource.data.upper()}_TERM_{form.term.data.upper()}_{form.year.data}.pdf")
            return f"{resource_text}"
        flash(error)
    return render_template("upload.html", form=form)



def is_valid_resource(file_descriptor):
    """
    Uses the `pymupdf` library to read buffer from stream and validate the file type.
    Returns `True` if its a valid PDF and `False` otherwise.
    """
    try:
        resource = pymupdf.Document(stream=BytesIO(file_descriptor.read()), filetype="pdf")
    except OSError as oe:
        abort(400, f"Server only accepts Buffer streams {oe}")
    try:
        if resource.is_pdf:
            return True
    except Exception as e:
        abort(e, f"You request cannot be processed. Please try again later. {e}")