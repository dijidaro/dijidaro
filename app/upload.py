from flask import Blueprint, current_app, render_template, flash
from forms import UploadForm
from werkzeug.utils import secure_filename
import os
import magic
from auth import login_required

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
        f = form.uploaded_resource.data
        if not is_valid_pdf(f):
            error = "Seems like the provided document is not a PDF file. Kindly check the instructions before uploading again."
        if error is None:
            filename = secure_filename(f"{form.school.data.upper()}_{form.subject.data.upper()}_{form.resource.data.upper()}_TERM_{form.term.data.upper()}_{form.year.data}.pdf")
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            print(file_path)
            print(filename)
            f.save(file_path)
            flash("File has been uploaded successfully")
            return render_template("resources.html")
        flash(error)
    return render_template("upload.html", form=form)


def is_valid_pdf(file_descriptor):
    """
    Uses the `python-magic` library to detect the MIME type of the uploaded file to verify if it's
     a PDF. Returns `true` if it is a PDF and `false` otherwise.
    """
    # Create a Magic object for MIME type detection
    mime_magic = magic.Magic(mime=True)

    # Detect the MIME type of the uploaded file
    mime_type = mime_magic.from_buffer(file_descriptor.read(2048))
    
    return mime_type == "application/pdf"
