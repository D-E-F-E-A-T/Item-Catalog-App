from flask import Flask, render_template, url_for, request, redirect, \
    flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Movie
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Get the client id from the json file
CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Movie Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///movies_database.db')
Base.metadata.bind = engine


def createUser(login_session):
    # Create new user in the database
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    newUser = User(name="", email=login_session['email'],
                        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    # This function takes the user_id as input and return the user
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    # This function take email as inpute and check
    # if a user is registred with this email
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Home page that shows all categories and movies
@app.route('/')
@app.route('/category')
def showCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    movies = session.query(Movie).all()
    return render_template('showCategories.html',
                           categories=categories, movies=movies)


# Create a new category
@app.route('/category/create', methods=['GET', 'POST'])
def createCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # Check if the user is logged in to create category
    if 'email' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash("Category Created")
        return redirect(url_for('showCategory'))
    else:
        return render_template("createCategory.html")


# Delete Category
@app.route('/category/delete', methods=['GET', 'POST'])
def deleteCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # Check if the user is logged in to delete category
    if 'email' not in login_session:
        return redirect('/login')
    categories = session.query(Category).filter_by(
        user_id=login_session['user_id']).all()
    if request.method == 'POST':
        deleteCategory = session.query(Category).filter_by(
            id=request.form['category']).one()
        session.delete(deleteCategory)
        session.commit()
        flash("Category Deleted")
        return redirect(url_for('showCategory'))
    else:
        return render_template("deleteCategory.html", categories=categories)


# Show a given category movies
@app.route('/category/<int:category_id>/movies')
def showCatergoryMovies(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    movies = session.query(Movie).filter_by(category_id=category_id).all()
    return render_template('showCategories.html',
                           categories=categories, movies=movies)


# Create a movie
@app.route('/category/movies/create', methods=['GET', 'POST'])
def createMovie():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).filter_by(
        user_id=login_session['user_id']).all()
    # Check if the user is logged in to create movie
    if 'email' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newMovie = Movie(name=request.form['name'],
                         description=request.form['description'],
                         photo=request.form['photo'],
                         trailer=request.form['trailer'],
                         user_id=login_session['user_id'],
                         category_id=request.form['category'])
        session.add(newMovie)
        session.commit()
        flash("Movie Created")
        return redirect(url_for('showCategory'))
    else:
        return render_template("createMovie.html", categories=categories)


# Show a specefic movie
@app.route('/category/movie/<int:movie_id>')
def showMovie(movie_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movie = session.query(Movie).filter_by(id=movie_id).one()
    # Get youtube video id
    id_string = movie.trailer
    vid_id = id_string.split("=")
    v_id = vid_id[1]
    return render_template('showMovie.html', movie=movie, v_id=v_id)


# Edit movie
@app.route('/category/movie/<int:movie_id>/edit', methods=['GET', 'POST'])
def editMovie(movie_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movie = session.query(Movie).filter_by(id=movie_id).one()
    categories = session.query(Category).filter_by(
        user_id=login_session['user_id']).all()
    # Check if the user is logged in to edit movie
    if 'email' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        editMovie = session.query(Movie).filter_by(id=movie_id).one()
        editMovie.name = request.form['name']
        editMovie.description = request.form['description']
        editMovie.trailer = request.form['trailer']
        editMovie.photo = request.form['photo']
        editMovie.category_id = request.form['category']
        session.add(editMovie)
        session.commit()
        flash("Movie Edited")
        return redirect(url_for('showCategory'))
    else:
        # Check if it's the user owner of the movie or another user
        if movie.user_id == login_session['user_id']:
            return render_template("editMovie.html",
                                   movie=movie, categories=categories)
        else:
            return render_template('notAuthorized.html')


# Delete movie
@app.route('/category/movie/<int:movie_id>/delete', methods=['GET', 'POST'])
def deleteMovie(movie_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movie = session.query(Movie).filter_by(id=movie_id).one()
    # Check if the user is logged in to edit movie
    if 'email' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        deleteMovie = session.query(Movie).filter_by(id=movie_id).one()
        session.delete(deleteMovie)
        session.commit()
        flash("Movie Deleted")
        return redirect(url_for('showCategory'))
    else:
        # Check if it's the user owner of the movie or another user
        if movie.user_id == login_session['user_id']:
            return render_template("deleteMovie.html", movie=movie)
        else:
            return render_template('notAuthorized.html')


# Login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Google+ Sing in
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user exists
    user_id = getUserID(login_session["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # An output to tell the user success of signing in
    output = ''
    output += '<h1>Welcome, '
    output += login_session['email']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; \
        border-radius: 150px;-webkit-border-radius: 150px; \
            -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['email'])
    return output


# Google+ logging out
@app.route('/gdisconnect')
def gdisconnect():
    if not login_session['email']:
        render_template('notAuthorized.html')
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s' % access_token
    print 'email is: %s' % login_session['email']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You're Logged Out")
        return redirect(url_for('showCategory'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON API to show all categories
@app.route('/categories/JSON')
def showCategoriesJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


# JSON API to show a category by its id
@app.route('/category/<int:category_id>/JSON')
def showCategoryJSON(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categorie = session.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=[categorie.serialize])


# JSON API to show all movies
@app.route('/categories/movies/JSON')
def showMoviesJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movies = session.query(Movie).all()
    return jsonify(Movie=[movie.serialize for movie in movies])


# JSON API to show a specific category movies
@app.route('/category/<int:category_id>/movies/JSON')
def showCategoryMoviesJSON(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movies = session.query(Movie).filter_by(category_id=category_id).all()
    return jsonify(Movie=[movie.serialize for movie in movies])


# JSON API to show a specific movie
@app.route('/category/<int:category_id>/movie/<int:movie_id>/JSON')
def showCategoryMovieJSON(category_id, movie_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movie = session.query(Movie).filter_by(
        category_id=category_id, id=movie_id).one()
    return jsonify(Movie=[movie.serialize])


# JSON API to show a specefic user movies
@app.route('/movies/<int:user_id>/JSON')
def showUserMoviesJSON(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movies = session.query(Movie).filter_by(user_id=user_id).all()
    return jsonify(Movie=[movie.serialize for movie in movies])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
