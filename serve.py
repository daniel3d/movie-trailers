import media
import webbrowser
from bottle import route, run, debug, template, request
from bottle import redirect, static_file, error

debug(False)

# Home Page (GET)
@route('/')
def index_page():
	output = template('index.tpl', movies = media.getAllMovies())
	return output

# New Movie (POST)
@route('/', method='POST')
def new_movie_post():
	media.createMovie( 
		request.POST.title.strip(), request.POST.story.strip(), 
		request.POST.poster.strip(), request.POST.trailer.strip())
	return redirect('/')

# Edit Movie (POST)
@route('/edit/<no:int>', method='POST')
def edit_movie_post(no):
	media.updateMovie(no, 
		request.POST.title.strip(), request.POST.story.strip(), 
		request.POST.poster.strip(), request.POST.trailer.strip())
	return redirect('/')

# Delete Movie (GET)
@route('/delete/<no:int>')
def delete_movie(no):
	media.deleteMovie(no)
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