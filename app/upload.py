from flask import Blueprint, current_app, render_template, flash, abort, redirect, url_for
from forms import UploadForm
from werkzeug.utils import secure_filename
import os
from auth import login_required
import pymupdf
from io import BytesIO
import json

bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=("GET", "POST"))
@login_required
def upload_resource():
    #TO DO
    # 1. Grab form data
    # 2. Check if file is indeed pdf. i.e use pdf signatures
    # 3. Check if file contents matches the grabbed form data
    # 4. Save the resource data to a database and the file to a file server storage.
    # 5. Redirect to a success page.
    form = UploadForm()
    if form.validate_on_submit():
        uploads_folder = current_app.config["UPLOAD_FOLDER"]
        resource_file = form.uploaded_resource.data
        resource_form_data = {
            "subject": form.subject.data.upper(),
            "school" : form.school.data.upper(),
            "term" : form.term.data.upper(),
            "year" : form.year.data        
        }
        missing_resource_form_data = {}
        resource_stream_data = pymupdf.Document(stream=BytesIO(resource_file.read()), filetype="pdf")
        resource_text = resource_stream_data[0].get_text("text").strip().upper()
        is_valid = is_valid_resource(resource_form_data, resource_text, missing_resource_form_data)
        if is_valid:
            resource_name = secure_filename(f"{resource_form_data['subject']}_{resource_form_data['school']}_{resource_form_data['term']}_{resource_form_data['year']}.pdf").lower()
            resource_path = os.path.join(uploads_folder, resource_name)
            resource_stream_data.save(resource_path)
            flash("Success :)")
            return render_template('explore.html', text=resource_text)
        flash(f"Error processing {json.dumps(missing_resource_form_data)}")
    return render_template("upload.html", form=form)

def is_valid_resource(form_data_dict, text, missing_values):
    for key, value in form_data_dict.items():
        if str(value) not in text:
            missing_values[key] = value
            return False
    return True
