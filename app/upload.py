from flask import Blueprint, current_app, render_template, flash, g, send_from_directory, url_for, redirect
from forms import UploadForm
from werkzeug.utils import secure_filename
import os
from auth import login_required
import pymupdf
from io import BytesIO
import time
from datetime import datetime
from models import Subject, School
import logging

bp = Blueprint("upload", __name__)

@bp.route("/upload", methods=("GET", "POST"))
@login_required
def upload_resource():
    # TO DO
    # 1. Grab form data
    # 2. Check if file is indeed pdf. i.e use pdf signatures
    # 3. Check if file contents matches the grabbed form data
    # 4. Save the resource data to a database and the file to a file server storage.
    # 5. Redirect to a success page.
    uploads_folder = current_app.config["UPLOAD_FOLDER"]
    start_time = time.time()
    form = UploadForm()
    data_list = {
        "subjects" : Subject().query.all(),
        "schools" : School().query.all()
    }

    if form.validate_on_submit():
        error = None
        try:
            resource = pymupdf.Document(stream=BytesIO(form.uploaded_resource.data.read()), filetype="pdf")
        except Exception as e:
            logging.error(f"Error: {e}")
            return f"Error reading file. Check logs fore more infow."
               
        form_data = {
            "category" : form.resource.data,
            "subject" : form.subject.data,
            "school" : form.school.data,
            "level": form.level.data,
            "term" : form.term.data,
            "year" : form.year.data,
        }
        
        missing_form_data = {}
        resource_first_page = resource[0]
        resource_text = extract_resource_text(resource_first_page)
        
        if resource_text is None:
            error = "An error occured during text extraction. Ensure the document is not corrupted."
        elif not is_valid_resource(form_data, resource_text, missing_form_data):
            error = f"The contents of the uploaded file do not match the information provided in the form. Please ensure that the file content correctly reflects the form data."
        
        if error is None:
            resource_name = secure_filename(f"{form_data['school']}_{form_data['category']}_{form_data['subject'][:4]}_{form_data['level']}_term_{form_data['term']}_{form_data['year']}.pdf").lower()
            resource_path = os.path.join(uploads_folder, resource_name)
            resource_pix = resource_first_page.get_pixmap()
            resource_thumb_name = secure_filename(f"{form_data['school']}_{form_data['category']}_{form_data['subject'][:4]}_{form_data['level']}_term_{form_data['term']}_{form_data['year']}.jpeg").lower()
            resource_thumb_path = os.path.join(uploads_folder, resource_thumb_name)
            form_data["resource_name"] = resource_name
            form_data["resource_url"] = resource_path
            form_data["thumbnail"] = resource_thumb_name
            form_data["thumbnail_url"] = resource_thumb_path
            form_data["uploaded_by"] = g.user.username
            form_data["date_uploaded"] = datetime.now()
            resource_pix.save(resource_thumb_path, output=None, jpg_quality=95)
            resource.save(resource_path)
            resource.close()
            end_time = time.time()
            execution_time = end_time - start_time
            flash("Resource uploaded successfully.")
            return redirect(url_for('explore.explore_resources'))
        flash(error)
    return render_template("upload.html", form=form, data=data_list)


@bp.route("/uploads/<filename>")
def uploaded_file(filename):
    uploads_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(uploads_folder, filename)


@bp.route("/download/<filename>")
def download_file(filename):
    uploads_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(uploads_folder, filename)



def is_valid_resource(form_data_dict, text, missing_values):
    """
    Checks if all values in the form_data_dict are present in the text. 
    If any value is missing, it adds it to the missing_values dictionary.

    Args:
        form_data_dict (dict): A dictionary containing form data to validate against the text.
        text (str): The text to search within.
        missing_values (dict): A dictionary to store missing values.

    Returns:
        bool: True if all values are found in the text, False otherwise.

    Example:
        >>> form_data = {"name": "Malcolm X", "email": "x.malcolm@example.com"}
        >>> text = "Malcolm X is the manager. You can reach him at x.malcolm@example.com."
        >>> missing_values = {}
        >>> is_valid_resource(form_data, text, missing_values)
        True
        >>> missing_values
        {}

        >>> form_data = {"name": "Malcolm X", "email": "x.malcolm@example.com"}
        >>> text = "Malcolm X is the manager. You can reach him at x.malcolm@example.com."
        >>> missing_values = {}
        >>> is_valid_resource(form_data, text, missing_values)
        False
        >>> missing_values
        {'name': 'Malcolm X', 'email': 'x.malcolm@example.com'}
    """

    for key, value in form_data_dict.items():
        if str(value).upper() not in text.upper():
            missing_values[key] = value
            return False
    return True


def extract_resource_text(page, tessdata_prefix = "/usr/share/tesseract-ocr/5/tessdata/", dpi=72, language="eng", full=False):
    """
    
    Extracts text from a page using pymupdf library and OCR with tesseract

    Args:
        page: The page object to extract text from. It should have methods get_textpage_ocr and get_text.
        tessdata_prefix (str): The path to the tessdata directory.
        dpi (int): The resolution in dots per inch to use for OCR.
        language (str): The language to use for OCR.

    Returns:
        str: The extracted text, or None if an error occurs.
    
    Example:
            >>> from unittest.mock import MagicMock
            >>> mock_page = MagicMock()
            >>> mock_page.get_textpage_ocr.return_value = "mock_text_page"
            >>> mock_page.get_text.return_value = "Mocked text content"
            >>> extract_resource_text(mock_page)
            'Mocked text content'
            >>> mock_page.get_textpage_ocr.assert_called_once_with(flags=0, dpi=72, language="eng", tessdata="/usr/share/tesseract-ocr/5/tessdata/", full=False)
            >>> mock_page.get_text.assert_called_once_with(textpage="mock_text_page", sort=True)

            >>> mock_page.get_textpage_ocr.side_effect = Exception("OCR error")
            >>> extract_resource_text(mock_page) is None
            True
    """
    try:
        logging.info(f"Using tessdata at: {tessdata_prefix}.")
        # print(tessdata_prefix)
        partial_text_page = page.get_textpage_ocr(flags=0, dpi=dpi, language=language, tessdata=tessdata_prefix, full=full)
        page_text = page.get_text(textpage=partial_text_page, sort=True).strip()
        return page_text
    except Exception as e:
        logging.error(f"Error processing the file: {e}.")
        return None
