import os

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from flask_app import app
from forms import UploadForm
from werkzeug.utils import secure_filename

from mining import process_file

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            support = form.support.data
            confidence = form.confidence.data
            f = form.transactions_file.data

            filename = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            f.save(path)
            process_file(path, filename, support, confidence)

            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('/index.html', form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], (filename), as_attachment=True)
