from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    entries = db.relationship('Diary', backref='logger', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)  

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_watched = db.Column(db.DateTime)
    movie_name = db.Column(db.String(200))
    release_date = db.Column(db.DateTime)
    user_rating = db.Column(db.Float())
    rewatch = db.Column(db.Boolean(create_constraint=False))
    review = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '{} -> Movie: {}, Released: {}, Rating: {}, Rewatch?: {} '.format(self.date_watched,self.movie_name), self.release_date, self.user_rating, self.rewatch)

        