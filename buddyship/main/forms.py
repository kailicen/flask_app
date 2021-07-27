from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class HomeForm(FlaskForm):
    buddy_role = SelectField('Your buddy\'s role', validators=[DataRequired()],
                             choices=[("Prepared Speech", "Prepared Speech"),
                                      ("Tabletopic Speech", "Tabletopic Speech"),
                                      ("Ah Counter", "Ah Counter"),
                                      ("Educational Role", "Educational Role"),
                                      ("General Evaluator", "General Evaluator"),
                                      ("Hark and Fine", "Hark and Fine"),
                                      ("Prepared Speech Evaluator",
                                       "Prepared Speech Evaluator"),
                                      ("Table Topic Evaluator",
                                       "Table Topic Evaluator"),
                                      ("Table Topic Master", "Table Topic Master"),
                                      ("Timer", "Timer"),
                                      ("Toast of the Day", "Toast of the Day"),
                                      ("Toastmaster", "Toastmaster"),
                                      ("Word of the Day/Grammarian", "Word of the Day/Grammarian")],)
    buddy_score = SelectField('Your buddy\'s score', validators=[DataRequired()],
                              choices=[('5-Exemplary', '5-Exemplary'),
                                       ('4-Excel', '4-Excel'),
                                       ('3-Accomplished', '3-Accomplished'),
                                       ('2-Emerging', '2-Emerging'),
                                       ('1-Developing', '1-Developing')])
    buddy_comment = TextAreaField('Comment', validators=[
        DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Submit')
