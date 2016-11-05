import sqlite3
from media import Movie
from bottle import route, run, debug, template, request, static_file, error

# List of all application routes

@route('/')
def index():

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movies")
    results = c.fetchall()
    c.close()

    movies = [Movie(res[1], res[2], res[3], res[4]) for res in results]

    output = template('index.tpl', movies = movies)
    return output

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(port=8888, reloader=True, host='localhost')
# remember to remove reloader=True and debug(True) when you move your
# application from development to a productive environment
