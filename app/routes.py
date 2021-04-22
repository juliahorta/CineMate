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
info_url = "https://api.themoviedb.org/3/movie/"

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
    users = User.query.order_by(User.username.desc()).all()
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_entries().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('home', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('home', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url, users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        users = User.query.order_by(User.username.desc()).all()
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
        users = User.query.order_by(User.username.desc()).all()
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('welcome_c'))
    return render_template('register.html', title='Register', form=form)

@app.route('/welcome')
def welcome_c():
    return render_template('tutorial.html')

@app.route('/user/<username>')
@login_required
def user(username):
    users = User.query.order_by(User.username.desc()).all()
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.entries.order_by(Diary.date_watched.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form, users=users)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    users = User.query.order_by(User.username.desc()).all()
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form, users=users)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    users = User.query.order_by(User.username.desc()).all()
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            # flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        # flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username, users=users))
    else:
        return redirect(url_for('index'), users=users)

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    users = User.query.order_by(User.username.desc()).all()
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'), users=users)
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username), users=users)
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username), users=users)
    else:
        return redirect(url_for('index'), users=users)
 
@app.route('/popular')
@login_required
def popular():
    users = User.query.order_by(User.username.desc()).all()
    conn = urllib.request.urlopen(popular_url)
    json_data = json.loads(conn.read())
    return render_template('popular.html', results=json_data["results"][:18], users=users)

# @app.route('/genre-rating', methods=['GET', 'POST'])
# def g_rate():
#     form = RateGenres()
#     if form.validate_on_submit():
#         ratings = GenreRating(action = form.action.data, adventure = form.adventure.data, animation = form.animation.data,
#             comedy = form.comedy.data, crime = form.war.data, documentary = form.war.data, drama = form.drama.data,
#             family = form.family.data, fantasy = form.fantasy.data, history = form.history.data, horror = form.horror.data,
#             music = form.music.data, mystery = form.mystery.data, romance = form.romance.data, scifi = form.scifi.data,
#             thriller = form.thriller.data, war = form.war.data, western = form.western.data, g_rater=current_user)
#         db.session.add(ratings)
#         db.session.commit()
#         return redirect(url_for('user', username=current_user.username))
#     return render_template('genre_rating.html', form=form)

@app.route('/search-movie', methods=['GET', 'POST'])
@login_required
def m_search():
    users = User.query.order_by(User.username.desc()).all()
    form = MovieSearch()
    if form.validate_on_submit():
        user_search = urllib.parse.quote(form.movieName.data)
        complete_url = search_url + user_search + "&page=1"
        conn = urllib.request.urlopen(complete_url)
        json_data = json.loads(conn.read())
        return render_template('search_results.html', results=json_data["results"], term=form.movieName.data, users=users)
    return render_template('movie_search.html', form=form, users=users)

@app.route('/search-movie-4-recc', methods=['GET', 'POST'])
@login_required
def rec_m_search():
    users = User.query.order_by(User.username.desc()).all()
    form = MovieSearch()
    if form.validate_on_submit():
        user_search = urllib.parse.quote(form.movieName.data)
        complete_url = search_url + user_search + "&page=1"
        conn = urllib.request.urlopen(complete_url)
        json_data = json.loads(conn.read())
        return render_template('rec_search_results.html', results=json_data["results"], term=form.movieName.data, users=users)
    return render_template('rec_search.html', form=form, users=users)

@app.route('/search-movie-2-4-recc', methods=['GET', 'POST'])
@login_required
def rec_m_search_2():
    users = User.query.order_by(User.username.desc()).all()
    movie1id = request.args['movie1id']
    form = MovieSearch()
    if form.validate_on_submit():
        user_search = urllib.parse.quote(form.movieName.data)
        complete_url = search_url + user_search + "&page=1"
        conn = urllib.request.urlopen(complete_url)
        json_data = json.loads(conn.read())
        return render_template('rec_search_results_2.html', results=json_data["results"], term=form.movieName.data, users=users, movie1id=movie1id)
    return render_template('rec_search2.html', form=form, users=users)

@app.route('/search-movie-3-4-recc', methods=['GET', 'POST'])
@login_required
def rec_m_search_3():
    users = User.query.order_by(User.username.desc()).all()
    movie1id = request.args['movie1id']
    movie2id = request.args['movie2id']
    form = MovieSearch()
    if form.validate_on_submit():
        user_search = urllib.parse.quote(form.movieName.data)
        complete_url = search_url + user_search + "&page=1"
        conn = urllib.request.urlopen(complete_url)
        json_data = json.loads(conn.read())
        return render_template('rec_search_results_3.html', results=json_data["results"], term=form.movieName.data, users=users, movie1id=movie1id, movie2id=movie2id)
    return render_template('rec_search3.html', form=form, users=users)

@app.route('/recommendation-1', methods=['GET', 'POST'])
@login_required
def rec_options_1():
    users = User.query.order_by(User.username.desc()).all()
    movieid = request.args['movieid']
    mname = request.args['mname']
    myear = request.args['myear']
    rec_url = info_url + movieid + "/recommendations?api_key=" + api_key + "&page=1"
    conn = urllib.request.urlopen(rec_url)
    json_data = json.loads(conn.read())
    return render_template('user_1_reccs.html', results=json_data["results"][:3], users=users)

@app.route('/recommendation-2', methods=['GET', 'POST'])
@login_required
def rec_options_2():
    users = User.query.order_by(User.username.desc()).all()
    movie1id = request.args['movie1id']
    movie2id = request.args['movie2id']

    rec_url1 = info_url + movie1id + "/recommendations?api_key=" + api_key + "&page=1"
    conn1 = urllib.request.urlopen(rec_url1)
    json_data1 = json.loads(conn1.read())
    movies_for_1 = json_data1["results"]

    rec_url2 = info_url + movie2id + "/recommendations?api_key=" + api_key + "&page=1"
    conn2 = urllib.request.urlopen(rec_url2)
    json_data2 = json.loads(conn2.read())
    movies_for_2 = json_data2["results"]

    json_data_total = []
    json_data_common = [d for d in movies_for_1 if d in movies_for_2]
    if not json_data_common:
        json_data_total = json_data1["results"][:3] + json_data2["results"][:3]
        

    return render_template('user_2_reccs.html', results=json_data_common[:3], seperate=json_data_total, users=users)

@app.route('/recommendation-3', methods=['GET', 'POST'])
@login_required
def rec_options_3():
    users = User.query.order_by(User.username.desc()).all()
    movie1id = request.args['movie1id']
    movie2id = request.args['movie2id']
    movie3id = request.args['movie3id']

    rec_url1 = info_url + movie1id + "/recommendations?api_key=" + api_key + "&page=1"
    conn1 = urllib.request.urlopen(rec_url1)
    json_data1 = json.loads(conn1.read())
    movies_for_1 = json_data1["results"]

    rec_url2 = info_url + movie2id + "/recommendations?api_key=" + api_key + "&page=1"
    conn2 = urllib.request.urlopen(rec_url2)
    json_data2 = json.loads(conn2.read())
    movies_for_2 = json_data2["results"]

    rec_url3 = info_url + movie3id + "/recommendations?api_key=" + api_key + "&page=1"
    conn3 = urllib.request.urlopen(rec_url3)
    json_data3 = json.loads(conn3.read())
    movies_for_3 = json_data3["results"]

    json_data_total = []
    json_data_common = [d for d in movies_for_1 if d in movies_for_2 or d in movies_for_3 and d != movie1id or movie2id or movie3id]
    if not json_data_common:
        json_data_total = json_data1["results"][:3] + json_data2["results"][:3] + json_data3["results"][:3]
        
    return render_template('user_3_reccs.html', results=json_data_common[:3], seperate=json_data_total, users=users)

@app.route('/log-movie', methods=['GET', 'POST'])
@login_required
def log_movie():
    users = User.query.order_by(User.username.desc()).all()
    movieid = request.args['movieid']
    mname = request.args['mname']
    myear = request.args['myear']
    mposter = request.args['mposter']
    log_url = info_url + movieid + "?api_key=" + api_key
    conn = urllib.request.urlopen(log_url)
    json_data = json.loads(conn.read())
    form = LogMovie()
    if form.validate_on_submit():
        log_data = Diary(date_watched=form.dateWatched.data, movie_name=mname, movie_id=movieid, poster_path=mposter, release_date=myear, user_rating=form.movieRating.data, 
            rewatch=form.movieRewatch.data, review=form.movieReview.data, logger=current_user)
        db.session.add(log_data)
        db.session.commit()
        return redirect(url_for('home'), users=users)
    return render_template('log_movie.html', form=form, result=json_data, users=users)

@app.route('/confirm-reccomendation', methods=['GET', 'POST'])
@login_required
def one_mov_rec():
    users = User.query.order_by(User.username.desc()).all()
    movieid = request.args['movieid']
    mname = request.args['mname']
    myear = request.args['myear']
    mposter = request.args['mposter']
    log_url = info_url + movieid + "?api_key=" + api_key
    conn = urllib.request.urlopen(log_url)
    json_data = json.loads(conn.read())
    return render_template('rec_choice_1.html', result=json_data, users=users)

@app.route('/confirm-reccomendation2', methods=['GET', 'POST'])
@login_required
def two_mov_rec():
    users = User.query.order_by(User.username.desc()).all()
    movie1id = request.args['movie1id']
    movie2id = request.args['movie2id']
    
    log_url = info_url + movie1id + "?api_key=" + api_key
    conn = urllib.request.urlopen(log_url)
    json_data_1 = json.loads(conn.read())

    log_url2 = info_url + movie2id + "?api_key=" + api_key
    conn2 = urllib.request.urlopen(log_url2)
    json_data_2 = json.loads(conn2.read())
    return render_template('rec_choice_2.html', result1=json_data_1, result2=json_data_2, users=users)

@app.route('/confirm-reccomendation3', methods=['GET', 'POST'])
@login_required
def three_mov_rec():
    users = User.query.order_by(User.username.desc()).all()
    movie1id = request.args['movie1id']
    movie2id = request.args['movie2id']
    movie3id = request.args['movie3id']
    
    log_url = info_url + movie1id + "?api_key=" + api_key
    conn = urllib.request.urlopen(log_url)
    json_data_1 = json.loads(conn.read())

    log_url2 = info_url + movie2id + "?api_key=" + api_key
    conn2 = urllib.request.urlopen(log_url2)
    json_data_2 = json.loads(conn2.read())

    log_url3 = info_url + movie3id + "?api_key=" + api_key
    conn3 = urllib.request.urlopen(log_url3)
    json_data_3 = json.loads(conn3.read())
    return render_template('rec_choice_3.html', result1=json_data_1, result2=json_data_2, result3=json_data_3, users=users)
