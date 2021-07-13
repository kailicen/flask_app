from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from buddyship import db, login_manager
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.sql import func


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    if_admin = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    current_buddy = db.Column(db.String(150))
    current_goal = db.Column(db.String(150))
    current_reward = db.Column(db.String(150))
    confirmed_at = db.Column(db.Date, nullable=False)

    buddies = db.relationship('Buddy', backref='owner', lazy=True)
    goals = db.relationship('Goal', backref='owner', lazy=True)
    record_progresses = db.relationship('Progress', backref='giver', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}', '{self.current_buddy}', '{self.current_goal}', '{self.current_reward}')"


class Buddy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buddy_name = db.Column(db.String(100), nullable=False)
    buddy_count = db.Column(db.Integer, default=1)
    start_date = db.Column(db.DateTime, default=func.now())
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buddy_progresses = db.relationship(
        'Progress', backref='receiver', lazy=True)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal_direction = db.Column(db.String(150))
    goal_statement = db.Column(db.String(150))
    goal_count = db.Column(db.Integer, default=1)
    goal_reward = db.Column(db.String(150))
    start_date = db.Column(db.DateTime, default=func.now())
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buddy_role = db.Column(db.String(150))
    buddy_score = db.Column(db.String(150))
    buddy_comment = db.Column(db.String(1500))
    date = db.Column(db.DateTime, default=func.now())
    # buddy_goal is buddy's general goal
    buddy_goal = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buddy_id = db.Column(db.Integer, db.ForeignKey('buddy.id'))
