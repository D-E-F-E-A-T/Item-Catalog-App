from flask import Flask, render_template, url_for,request,redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Movie

app = Flask(__name__)

#Connect to Database and create database session
engine = create_engine('sqlite:///movies_database.db')
Base.metadata.bind = engine

@app.route('/')
@app.route('/category')
def showCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    movies = session.query(Movie).all()
    return render_template('showCategories.html', categories = categories, movies = movies)

@app.route('/category/create', methods = ['GET','POST'])
def createCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newCategory = Category(name = request.form['name'], user_id = 1)
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategory'))
    else:
        return render_template("createCategory.html")

@app.route('/category/delete', methods = ['GET','POST'])
def deleteCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    if request.method == 'POST':
        deleteCategory = session.query(Category).filter_by(id = request.form['category']).one()
        session.delete(deleteCategory)
        session.commit()
        return redirect(url_for('showCategory'))
    else:
        return render_template("deleteCategory.html", categories = categories)

@app.route('/category/<int:category_id>/movies')
def showCatergoryMovies(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    movies = session.query(Movie).filter_by(category_id=category_id).all()
    return render_template('showCategories.html', categories = categories, movies = movies)

@app.route('/category/movies/create', methods = ['GET','POST'])
def createMovie():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    if request.method == 'POST':
        newMovie = Movie(name = request.form['name'],description = request.form['description'], photo = request.form['photo'], trailer = request.form['trailer'], user_id = 1, category_id = request.form['category'])
        session.add(newMovie)
        session.commit()
        return redirect(url_for('showCategory'))
    else:
        return render_template("createMovie.html", categories = categories)

@app.route('/category/movie/<int:movie_id>')
def showMovie(movie_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movie = session.query(Movie).filter_by(id = movie_id).one()
    id_string = movie.trailer
    vid_id = id_string.split("=")
    v_id = vid_id[1]
    return render_template('showMovie.html',movie = movie, v_id = v_id)

@app.route('/category/movie/<int:movie_id>/edit', methods = ['GET','POST'])
def editMovie(movie_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movie = session.query(Movie).filter_by(id = movie_id).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        editMovie = session.query(Movie).filter_by(id = movie_id).one()
        editMovie.name = request.form['name']
        editMovie.description = request.form['description']
        editMovie.trailer = request.form['trailer']
        editMovie.photo = request.form['photo']
        editMovie.category_id = request.form['category']
        session.add(editMovie)
        session.commit()
        return redirect(url_for('showCategory'))
    else:
        return render_template("editMovie.html", movie = movie, categories = categories)

@app.route('/category/movie/<int:movie_id>/delete', methods = ['GET','POST'])
def deleteMovie(movie_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    movie = session.query(Movie).filter_by(id = movie_id).one()
    if request.method == 'POST':
        deleteMovie = session.query(Movie).filter_by(id = movie_id).one()
        session.delete(deleteMovie)
        session.commit()
        return redirect(url_for('showCategory'))
    else:
        return render_template("deleteMovie.html", movie = movie)

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)


