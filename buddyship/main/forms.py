from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class HomeForm(FlaskForm):
    buddy_role = SelectField('Your buddy\'s role', validators=[DataRequired()],
                             choices=[("Prepared speech", "Prepared speech"),
                                      ("Tabletopic speech", "Tabletopic speech"),
                                      ("Ah counter", "Ah counter"),
                                      ("Educational role", "Educational role"),
                                      ("General evaluator", "General evaluator"),
                                      ("Hark and fine", "Hark and fine"),
                                      ("Prepared speech evaluator",
                                       "Prepared speech evaluator"),
                                      ("Table topic evaluator",
                                       "Table topic evaluator"),
                                      ("Table topic master", "Table topic master"),
                                      ("Timer", "Timer"),
                                      ("Toast of the day", "Toast of the day"),
                                      ("Toastmaster", "Toastmaster"),
                                      ("Word of the day/Grammarian", "Word of the day/Grammarian")],)
    buddy_score = SelectField('Your buddy\'s score', validators=[DataRequired()],
                              choices=[('5-Exemplary', '5-Exemplary'),
                                       ('4-Excel', '4-Excel'),
                                       ('3-Accomplished', '3-Accomplished'),
                                       ('2-Emerging', '2-Emerging'),
                                       ('1-Developing', '1-Developing')])
    buddy_comment = TextAreaField('Comment', validators=[
        DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Submit')
