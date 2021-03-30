from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin
from app import db, login

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

genre_ratings = db.Table('genre_ratings',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')), 
    db.Column('action', db.Integer),
    db.Column('adventure', db.Integer),
    db.Column('animation', db.Integer),
    db.Column('comedy', db.Integer),
    db.Column('crime', db.Integer),
    db.Column('documentary', db.Integer),
    db.Column('drama', db.Integer),
    db.Column('family', db.Integer),
    db.Column('fantasy', db.Integer),
    db.Column('history', db.Integer),
    db.Column('horror', db.Integer),
    db.Column('music', db.Integer),
    db.Column('mystery', db.Integer),
    db.Column('romance', db.Integer),
    db.Column('sci-fi', db.Integer),
    db.Column('thriller', db.Integer),
    db.Column('war', db.Integer),
    db.Column('western', db.Integer)
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
    u_g_ratings = db.relationship(
        'User', secondary=genre_ratings,
        primaryjoin=(genre_ratings.c.user_id == id),
        backref=db.backref('g_ratings', lazy='dynamic'), lazy='dynamic')
    

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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_watched = db.Column(db.DateTime)
    movie_name = db.Column(db.String(200))
    release_date = db.Column(db.DateTime)
    user_rating = db.Column(db.Integer())
    rewatch = db.Column(db.Boolean(create_constraint=False))
    review = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<{} -> Movie: {}, Released: {}, Rating: {}, Rewatch?: {}>'.format(self.date_watched,self.movie_name, self.release_date, self.user_rating, self.rewatch)

# class Genre_Rating(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     g_act = 
#     g_adven
#     g_anim
#     g_com
#     g_crime
#     g_docu
#     g_drama
#     g_fam
#     g_fant
#     g_hist
#     g_horr
#     g_mus
#     g_myst
#     g_rom
#     g_scifi
#     g_thri
#     g_war
#     g_west
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))