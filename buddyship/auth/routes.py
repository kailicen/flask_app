from flask_admin.contrib import sqla
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user
from buddyship import db, bcrypt, mail, admin
from buddyship.models import Buddy, User
from buddyship.auth.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_mail import Message
from flask_admin.menu import MenuLink
from datetime import date
from flask_admin.model import typefmt
from sqlalchemy.sql import func


auth = Blueprint('auth', __name__)


def date_format(view, value):
    return value.strftime('%d/%m/%Y')


DATE_FORMATER = dict(typefmt.BASE_FORMATTERS)
DATE_FORMATER.update({
    date: date_format
})


class AdminHomeView(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))


class UserView(AdminHomeView):
    def update_model(self, form, model):
        try:
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to update record. %(error)s', 'error')

            self.session.rollback()

            return False
        else:
            if form.current_buddy is None:
                pass
            else:
                old_buddy = model.current_buddy
                new_buddy = form.current_buddy.data
                if new_buddy != old_buddy:
                    former_buddy_count = Buddy.query.filter_by(
                        user_id=model.id).count()

                    last_buddy = Buddy.query.filter_by(
                        user_id=model.id, buddy_count=former_buddy_count).first()

                    new_buddy_name = new_buddy.lower().title()
                    new_buddy_count = former_buddy_count + 1

                    last_buddy.end_date = func.now()
                    add_buddy = Buddy(buddy_name=new_buddy_name,
                                      buddy_count=new_buddy_count, user_id=model.id)
                    db.session.add(add_buddy)
                    db.session.commit()
            self.after_model_change(form, model, False)
        return True

    column_type_formatters = DATE_FORMATER
    column_editable_list = ['if_admin', 'active', 'email', 'first_name',
                            'current_buddy']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password', 'current_reward']
    #form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list
    form_edit_rules = ('if_admin', 'active', 'first_name', 'email',
                       'current_buddy')

    can_export = True
    edit_modal = True
    details_modal = True
    can_view_details = True
    can_delete = False
    can_create = False


class AdminLogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email == 'vppr-6247@toastmastersclubs.org'


class UserLogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email != 'vppr-6247@toastmastersclubs.org'


admin.add_view(UserView(User, db.session))
admin.add_link(AdminLogoutMenuLink(name='Logout', category='', url="/logout"))
admin.add_link(UserLogoutMenuLink(name='Logout', category='', url="/"))


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(if_admin=False, first_name=form.first_name.data.lower().title(),
                    email=form.email.data, password=hashed_password, active=True,
                    confirmed_at=date.today())
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.email == 'vppr-6247@toastmastersclubs.org':
                return redirect(url_for('admin.index'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@buddyship.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no change will be made.
'''
    mail.send(msg)


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
