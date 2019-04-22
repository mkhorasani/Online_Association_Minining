from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import DecimalField, SubmitField
from wtforms.validators import NumberRange

ALLOWED_EXTENSIONS = ['txt']

class UploadForm(FlaskForm):
    transactions_file = FileField("Transactions File", validators=[
        FileRequired(),
        FileAllowed(ALLOWED_EXTENSIONS, 'Text files only')
    ])

    support = DecimalField('Minimum Support', places=None, default=0.01,
        validators=[NumberRange(min=0)])

    confidence = DecimalField('Minimum Confidence', places=None, default=0,
        validators=[NumberRange(min=0)])

    submit = SubmitField('Upload')
