from flask import Blueprint, current_app, render_template
from forms import UploadForm
from werkzeug.utils import secure_filename
import os

bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=("GET", "POST"))
def upload_resource():
    # 1. Grab form data
    # 2. Check if file is indeed pdf. i.e use pdf signatures
    # 3. Check if file contents matches the grabbed form data
    # 4. Save the resource data to a database and the file to a file server storage.
    # 5. Redirect to a success page.
    
    form = UploadForm()
    
    if form.validate_on_submit():
        f = form.uploaded_resource.data
        if f.filename != "":
            filename = secure_filename(f"{form.school.data.upper()}_{form.subject.data.upper()}_{form.resource.data.upper()}_TERM_{form.term.data.upper()}_{form.year.data}.pdf")
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            print(file_path)
            f.save(file_path)
        print(filename)
        return render_template("resources.html")
    print(form.errors) 
    return render_template("upload.html", form=form)
