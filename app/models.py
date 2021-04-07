from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin
from app import db, login

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    entries = db.relationship('Diary', backref='logger', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    user_genre_ratings = db.relationship('GenreRating', backref='g_rater', lazy='dynamic')
    # u_g_ratings = db.relationship(
    #     'User', secondary=genre_ratings,
    #     primaryjoin=(genre_ratings.c.user_id == id),
    #     backref=db.backref('g_ratings', lazy='dynamic'), lazy='dynamic')
    

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)  
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_entries(self):
        followed = Diary.query.join(
            followers, (followers.c.followed_id == Diary.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Diary.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Diary.date_watched.desc())
    
    # def rate(self, initial_g_ratings):
    #     self.u_g_ratings.append(initial_g_ratings)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_watched = db.Column(db.String(140)) 
    movie_name = db.Column(db.String(200))
    release_date = db.Column(db.Integer())
    user_rating = db.Column(db.Integer())
    rewatch = db.Column(db.Boolean(create_constraint=False))
    review = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<{} -> Movie: {}, Released: {}, Rating: {}, Rewatch?: {}>'.format(self.date_watched,self.movie_name, self.release_date, self.user_rating, self.rewatch)

class GenreRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Integer)
    adventure = db.Column(db.Integer)
    animation = db.Column(db.Integer)
    comedy = db.Column(db.Integer)
    crime = db.Column(db.Integer)
    documentary = db.Column(db.Integer)
    drama = db.Column(db.Integer)
    family = db.Column(db.Integer)
    fantasy = db.Column(db.Integer)
    history = db.Column(db.Integer)
    horror = db.Column(db.Integer)
    music = db.Column(db.Integer)
    mystery = db.Column(db.Integer)
    romance = db.Column(db.Integer)
    scifi = db.Column(db.Integer)
    thriller = db.Column(db.Integer)
    war = db.Column(db.Integer)
    western = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
