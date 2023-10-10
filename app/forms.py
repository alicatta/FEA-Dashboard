from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    model_name = StringField('Model Name', validators=[DataRequired()])
    location_name = StringField('Location Name', validators=[DataRequired()])
    file = FileField('Upload CSV', validators=[DataRequired()])
    submit = SubmitField('Upload')
