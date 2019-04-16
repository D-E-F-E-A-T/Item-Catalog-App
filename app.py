from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/category')
def showCategory():
    return "here you'll find categories"

@app.route('/category/create')
def createCategory():
    return "here you'll create categories"

@app.route('/category/<int:category_id>/movies')
def showCatergoryMovies():
    return "here you'll see category's movies"

@app.route('/category/<int:category_id>/movies/create')
def createMovie():
    return "here you'll create movie"

@app.route('/category/<int:category_id>/movie/<int:movie_id>')
def showMovie():
    return "here you'll see a movie"

@app.route('/category/<int:category_id>/movie/<int:movie_id>/edit')
def editMovie():
    return "here you'll edit a movie"

@app.route('/category/<int:category_id>/movie/<int:movie_id>/delete')
def deleteMovie():
    return "here you'll delete a movie"

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)


