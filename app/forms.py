from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class CreateScrutinForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    start_date = DateField('Date de début', validators=[DataRequired()])
    end_date = DateField('Date de fin', validators=[DataRequired()])
    options = StringField('Options (séparées par des virgules)', validators=[DataRequired()])
    submit = SubmitField('Créer le scrutin')