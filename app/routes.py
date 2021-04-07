from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, RateGenres, LogMovie, MovieSearch
from app.models import User, Diary, GenreRating
from datetime import datetime
import json
import urllib.request


api_key = "c927d9d9994588e8e9c580276b5305b5"
popular_url = "https://api.themoviedb.org/3/movie/popular?api_key=" + api_key + "&language=en-US"
search_url = "https://api.themoviedb.org/3/search/movie?api_key=" + api_key + "&query=" 


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
def default():
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():

    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
 
@app.route('/popular')
def popular():
    conn = urllib.request.urlopen(popular_url)
    json_data = json.loads(conn.read())
    return render_template('popular.html', results=json_data["results"])

@app.route('/genre-rating', methods=['GET', 'POST'])
def g_rate():
    form = RateGenres()
    if form.validate_on_submit():
        ratings = GenreRating(action = form.action.data, adventure = form.adventure.data, animation = form.animation.data,
            comedy = form.comedy.data, crime = form.war.data, documentary = form.war.data, drama = form.drama.data,
            family = form.family.data, fantasy = form.fantasy.data, history = form.history.data, horror = form.horror.data,
            music = form.music.data, mystery = form.mystery.data, romance = form.romance.data, scifi = form.scifi.data,
            thriller = form.thriller.data, war = form.war.data, western = form.western.data, g_rater=current_user)
        db.session.add(ratings)
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    return render_template('genre_rating.html', form=form)

@app.route('/search-movie', methods=['GET', 'POST'])
def m_search():
    form = MovieSearch()
    if form.validate_on_submit():
        user_search = urllib.parse.quote(form.movieName.data)
        complete_url = search_url + user_search + "&page=1"
        conn = urllib.request.urlopen(complete_url)
        json_data = json.loads(conn.read())
        return render_template('search_results.html', results=json_data["results"], term=form.movieName.data)
    return render_template('movie_search.html', form=form)
