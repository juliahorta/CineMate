from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.fields.html5 import DateField
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class RateGenres(FlaskForm):
    action = RadioField('Action', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    adventure = RadioField('Adventure', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    animation = RadioField('Animation', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    comedy = RadioField('Comedy', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    crime = RadioField('Crime', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    documentary = RadioField('Documentary', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    drama = RadioField('Drama', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    family = RadioField('Family', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    fantasy = RadioField('Fantasy', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    history = RadioField('History', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    horror = RadioField('Horror', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    music = RadioField('Music', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    mystery = RadioField('Mystery', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    romance = RadioField('Romance', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    scifi = RadioField('Sci-Fi', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    thriller = RadioField('Thriller', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    war = RadioField('War', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])
    western = RadioField('Western', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')])

    submit = SubmitField('Done')

class LogMovie(FlaskForm):
    # will already have movie name and release date info from api
    dateWatched = DateField('Date Watched', format='%Y-%m-%d', validators=[DataRequired()])
    movieReview = TextAreaField('Review', validators=[Length(min=0, max=140)], render_kw={"placeholder": "Write a review..."})
    movieRating = RadioField('Rating', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')], validators=[DataRequired()])
    movieRewatch = BooleanField('Rewatch?')
    submit = SubmitField('Save')

class MovieSearch(FlaskForm):
    movieName = StringField('Name of film', validators=[DataRequired()])
    submit = SubmitField('Search')