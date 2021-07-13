from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user, login_required
from buddyship.models import User, Buddy
from datetime import date
progresses = Blueprint('progresses', __name__)


@progresses.route('/my_progress', methods=['GET'])
@login_required
def my_progress():
    if current_user.current_buddy == None:
        flash('Please set up your buddy and your goal first. ', 'danger')
        return redirect(url_for('users.set_up'))
    else:
        buddies = Buddy.query.filter_by(
            buddy_name=current_user.first_name).all()
        id_lst = []
        for buddy in buddies:
            id_lst.append(buddy.user_id)

        return render_template("my_progress.html", title='My Progress', user=current_user,
                               buddy_accounts=User.query.filter(
                                   User.id.in_(id_lst)).all(),
                               current_time=date.today())


@progresses.route('/buddy_progress', methods=['GET'])
@login_required
def buddy_progress():
    if current_user.current_buddy == None:
        flash('Please set up your buddy and your goal first. ', 'danger')
        return redirect(url_for('users.set_up'))
    else:
        return render_template("buddy_progress.html", title='Buddy\'s Progress', user=current_user)
