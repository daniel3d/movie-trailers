import media
import webbrowser
from bottle import route, run, debug, template, request
from bottle import redirect, static_file, error

debug(False)

# Home Page (GET)


@route('/')
def index_page():
    movies = media.getAllMovies()
    output = template('index.tpl', movies=movies)
    return output

# New Movie (POST)


@route('/', method='POST')
def new_movie_post():
    movie = media.Movie(
        request.POST.title.strip(),
        request.POST.story.strip(),
        request.POST.poster.strip(),
        request.POST.trailer.strip()
    )
    movie.save()
    return redirect('/')

# Edit Movie (POST)


@route('/edit/<no:int>', method='POST')
def edit_movie_post(no):
    movie = media.getMovieById(no)
    movie.title = request.POST.title.strip()
    movie.story = request.POST.story.strip()
    movie.poster = request.POST.poster.strip()
    movie.trailer = request.POST.trailer.strip()
    movie.save()
    return redirect('/')

# Delete Movie (GET)


@route('/delete/<no:int>')
def delete_movie(no):
    movie = media.getMovieById(no)
    movie.delete()
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
