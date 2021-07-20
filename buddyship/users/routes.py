from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from buddyship import db
from buddyship.models import Buddy, Goal
from buddyship.users.forms import SetUpAccountForm, UpdateAccountForm
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy.sql import func
users = Blueprint('users', __name__)


@users.route("/set_up", methods=['GET', 'POST'])
@login_required
def set_up():
    form = SetUpAccountForm()
    if form.validate_on_submit():
        general_goal = form.general_goal.data
        specific_goal = form.specific_goal.data
        goal_reward = form.reward.data

        current_user.current_buddy = form.buddy_first_name.data.strip().lower().title()
        current_user.current_general_goal = general_goal
        current_user.current_specific_goal = specific_goal
        current_user.current_reward = form.reward.data

        end_date = date.today() + relativedelta(months=+6)

        new_buddy = Buddy(buddy_name=form.buddy_first_name.data.strip().lower().title(),
                          user_id=current_user.id)
        new_goal = Goal(general_goal=general_goal, specific_goal=specific_goal, goal_reward=goal_reward,
                        end_date=end_date, user_id=current_user.id)
        db.session.add(new_buddy)
        db.session.add(new_goal)
        db.session.commit()

        # check if your buddy has set up their account
        if Buddy.query.filter_by(buddy_name=current_user.first_name).first():
            flash('Things are all set!', 'success')
        return redirect(url_for('main.home'))
    return render_template("set_up.html", title='Set up', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data.strip().lower().title()
        current_user.email = form.email.data.lower()

        db.session.commit()

        # check if buddy changed
        if form.buddy_first_name.data.strip().lower().title() != current_user.current_buddy:
            former_buddy_count = Buddy.query.filter_by(
                user_id=current_user.id).count()

            last_buddy = Buddy.query.filter_by(
                user_id=current_user.id, buddy_count=former_buddy_count).first()

            new_buddy_name = form.buddy_first_name.data.strip().lower().title()
            new_buddy_count = former_buddy_count + 1

            current_user.current_buddy = new_buddy_name
            last_buddy.end_date = func.now()
            new_buddy = Buddy(buddy_name=new_buddy_name,
                              buddy_count=new_buddy_count, user_id=current_user.id)
            db.session.add(new_buddy)
            db.session.commit()

        # check if goal changed
        former_goal_count = Goal.query.filter_by(
            user_id=current_user.id).count()
        last_goal = Goal.query.filter_by(
            user_id=current_user.id, goal_count=former_goal_count).first()
        if form.specific_goal.data == current_user.current_specific_goal:
            if form.reward.data == current_user.current_reward:
                pass
            else:
                new_goal_reward = form.reward.data
                current_user.current_reward = new_goal_reward
                last_goal.goal_reward = new_goal_reward
                db.session.commit()

        else:
            new_general_goal = form.general_goal.data
            new_specific_goal = form.specific_goal.data
            new_goal_count = former_goal_count + 1
            new_goal_reward = form.reward.data
            new_end_date = date.today() + relativedelta(months=+6)

            current_user.current_general_goal = new_general_goal
            current_user.current_specific_goal = new_specific_goal
            last_goal.end_date = func.now()
            new_goal = Goal(general_goal=new_general_goal, specific_goal=new_specific_goal, goal_reward=new_goal_reward,
                            goal_count=new_goal_count, end_date=new_end_date, user_id=current_user.id)
            db.session.add(new_goal)
            db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.email.data = current_user.email
        form.buddy_first_name.data = current_user.current_buddy
        # not sure selectfield
        form.general_goal.data = current_user.current_general_goal
        form.specific_goal.data = current_user.current_specific_goal
        form.reward.data = current_user.current_reward

    return render_template('account.html', title='Account', form=form)
