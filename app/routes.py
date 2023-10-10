from flask import Blueprint, render_template, request, current_app as app, redirect, url_for
from app.utils import data_loader, data_processor
from app.forms import UploadForm
from werkzeug.utils import secure_filename
import os
from app import models

main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
@main.route('/dashboard')
def dashboard():
    models_list = models.ModelMetadata.query.all()
    return render_template('dashboard.html', models=models_list)

@main.route('/model/<model_name>/<location_name>')
def model_detail(model_name, location_name):
    data = data_loader.load_model_data(model_name, location_name)
    if not data:
        return render_template('error.html', error_message="Data not found"), 404

    processed_data = data_processor.process_data_for_visualization(data)
    return render_template('model_detail.html', model_data=processed_data)

@main.route('/model/<model_name>')
def model_overview(model_name):
    locations = data_loader.list_locations(model_name)
    if not locations:
        return render_template('error.html', error_message="Locations not found"), 404
    return render_template('model_overview.html', model_name=model_name, locations=locations)

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="Page not found"), 404

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            model_name = secure_filename(form.model_name.data)
            location_name = secure_filename(form.location_name.data)
            filename = f"{location_name}.csv"
            file_path = os.path.join(UPLOAD_FOLDER, model_name)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file.save(os.path.join(file_path, filename))
            # Add metadata to the database
            model_data = models.ModelMetadata(name=model_name, description="Some description")
            models.db.session.add(model_data)
            models.db.session.commit()
            return redirect(url_for('main.dashboard'))
    return render_template('upload.html', form=form)

@main.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query')
    models_results = models.ModelMetadata.query.filter(models.ModelMetadata.name.contains(query)).all()
    return render_template('search_results.html', results=models_results)
