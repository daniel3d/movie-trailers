import sqlite3
import webbrowser
from media import Movie
from bottle import route, run, debug, template, request
from bottle import redirect, static_file, error

debug(False)

# Home Page (GET)
@route('/')
def index_page():

    # Database
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movies")
    results = c.fetchall()
    c.close()

    # Load all movies with data from the movies.db 
    # (id, title, storyline, poster_image_url, trailer_url)
    movies = [Movie(res[0], res[1], res[2], res[3], res[4]) for res in results]

    # Render the Fresh Tomatoes Movie Trailers page
    output = template('index.tpl', movies = movies)
    return output

# New Movie (POST)
@route('/', method='POST')
def new_movie_post():

        title = request.POST.title.strip()
        story = request.POST.story.strip()
        poster = request.POST.poster.strip()
        trailer = request.POST.trailer.strip()

        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO movies (title,story,poster,trailer) VALUES (?,?,?,?)
            ''', (title,story,poster,trailer))
        conn.commit()
        c.close()

        # Go back to home page
        return redirect('/')

# Edit Movie (POST)
@route('/edit/<no:int>', method='POST')
def edit_movie_post(no):

        title = request.POST.title.strip()
        story = request.POST.story.strip()
        poster = request.POST.poster.strip()
        trailer = request.POST.trailer.strip()

        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        c.execute('''
            UPDATE movies SET title = ?, story = ?, poster = ?, trailer = ? 
            WHERE id = ? 
        ''', (title,story,poster,trailer,no))
        conn.commit()

        # Go back to home page
        return redirect('/')

# Delete Movie (GET)
@route('/delete/<no:int>')
def delete_movie(no):

        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        c.execute("DELETE FROM movies WHERE id = ?", (no,))
        conn.commit()

        # Go back to home page
        return redirect('/')

# Error Handling
@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

# Start the app
webbrowser.open("http://localhost:8888")
run(port=8888, reloader=False, host='localhost')