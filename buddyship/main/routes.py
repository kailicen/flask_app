from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import current_user, login_required
from buddyship import db
from buddyship.models import User, Buddy, Progress
from buddyship.main.forms import HomeForm
main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if current_user.current_buddy == None:
        flash('Please set up your buddy and your goal first. ', 'danger')
        return redirect(url_for('users.set_up'))
    else:
        set_buddy = Buddy.query.filter_by(user_id=current_user.id).first()
        if set_buddy:
            if set_buddy.buddy_name != current_user.current_buddy:
                set_buddy.buddy_name = current_user.current_buddy.lower().title()
                db.session.commit()
            else:
                pass
        else:
            add_buddy = Buddy(buddy_name=current_user.current_buddy.lower().title(),
                              user_id=current_user.id)
            db.session.add(add_buddy)
            db.session.commit()

        buddy_account = User.query.filter_by(
            first_name=current_user.current_buddy).first()
        if buddy_account == None:
            return redirect(url_for('main.stop'))
        else:
            form = HomeForm()
            if buddy_account.current_goal == None:
                return redirect(url_for('main.stop'))
            else:
                if form.validate_on_submit():
                    user_buddy = Buddy.query.filter_by(
                        buddy_name=current_user.current_buddy, user_id=current_user.id, end_date=None).first()
                    progress = Progress(buddy_role=form.buddy_role.data, buddy_score=form.buddy_score.data,
                                        buddy_comment=form.buddy_comment.data, buddy_goal=buddy_account.current_goal.split(
                                            ' - ')[0],
                                        user_id=current_user.id, buddy_id=user_buddy.id)
                    db.session.add(progress)
                    db.session.commit()
                    flash('Your buddy\'s progress is added!', 'success')
                    return redirect(url_for('progresses.buddy_progress'))
    return render_template("home.html", form=form, user=current_user, buddy_account=buddy_account)


@main.route("/stop")
@login_required
def stop():
    return render_template("stop.html", title='Wait')


@main.route('/tm_fam', methods=['GET'])
@login_required
def tm_fam():
    if current_user.current_buddy == None:
        flash('Please set up your buddy and your goal first. ', 'danger')
        return redirect(url_for('users.set_up'))
    else:
        all_users = User.query.with_entities(
            User.first_name, User.current_goal, User.current_buddy).all()
        buddyships_double = []
        goals_double = []
        for user1 in all_users:
            for user2 in all_users:
                if user1.first_name == user2.current_buddy:
                    if user2.first_name == user1.current_buddy:
                        buddyships_double.append(
                            user1.first_name + " & " + user2.first_name)
                        goals_double.append(
                            user1.current_goal + " & " + user2.current_goal)
        buddy_check = []
        buddyships = []
        for buddyship in buddyships_double:
            buddy1 = buddyship.split(" & ")[0]
            buddy2 = buddyship.split(" & ")[1]
            if buddy1 not in buddy_check:
                buddy_check.append(buddy1)
                buddy_check.append(buddy2)
                buddyships.append(buddyship)
        goal_check = []
        goals = []
        for goal in goals_double:
            goal1 = goal.split(" & ")[0]
            goal2 = goal.split(" & ")[1]
            if goal1 not in goal_check:
                goal_check.append(goal1)
                goal_check.append(goal2)
                goals.append(goal)
        count = len(buddyships)
        return render_template("tm_fam.html", title='Toastmasters Family', user=current_user, buddyships=buddyships, goals=goals, count=count)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
