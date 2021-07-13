from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from buddyship.models import User


class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    buddy_first_name = StringField('Your buddy\'s first name',
                                   validators=[DataRequired(), Length(min=2, max=20)])
    general_goal = SelectField('Select your general goal', validators=[DataRequired()],
                               choices=[("Audience Awareness",
                                         "Audience Awareness"),
                                        ("Clarity", "Clarity"),
                                        ("Eye contact", "Eye contact"),
                                        ("Filler words", "Filler words"),
                                        ("Gestures", "Gestures"),
                                        ("Vocal Variety", "Vocal Variety"),
                                        ("Others", "Others")])
    specific_goal = StringField('Your specific goal',
                                validators=[DataRequired(), Length(min=2, max=100)])
    reward = StringField('Your reward when you accomplish your goal',
                         validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Update')

    def validate_first_name(self, first_name):
        if first_name.data != current_user.first_name:
            user = User.query.filter_by(first_name=first_name.data).first()
            if user:
                raise ValidationError(
                    'That first name is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class SetUpAccountForm(FlaskForm):
    buddy_first_name = StringField('Your buddy\'s first name',
                                   validators=[DataRequired(), Length(min=2, max=20)])
    general_goal = SelectField('Select your general goal', validators=[DataRequired()],
                               choices=[("Audience Awareness",
                                         "Audience Awareness"),
                                        ("Clarity", "Clarity"),
                                        ("Eye contact", "Eye contact"),
                                        ("Filler words", "Filler words"),
                                        ("Gestures", "Gestures"),
                                        ("Vocal Variety", "Vocal Variety"),
                                        ("Others", "Others")])
    specific_goal = StringField('Your specific goal',
                                validators=[DataRequired(), Length(min=2, max=100)])
    reward = StringField('Your reward when you accomplish your goal',
                         validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Submit')

    def validate_buddy_first_name(self, buddy_first_name):
        user = User.query.filter_by(
            current_buddy=buddy_first_name.data).first()
        if user:
            raise ValidationError(
                'That buddy is taken. Please choose a different one.')
