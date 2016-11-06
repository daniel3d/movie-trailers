import sqlite3

database = sqlite3.connect('movies.db')

def getDBCursor():
	return database.cursor() 

class Movie():
	def __init__(self, id, title, story, poster_image_url, trailer_url):
		self.id = id
		self.title = title
		self.story = story
		self.poster_image_url = poster_image_url
		self.trailer_youtube_id = trailer_url
 
def getAllMovies():
	cursor = getDBCursor()
	cursor.execute('''SELECT * FROM movies''')
	results = cursor.fetchall()
	cursor.close()
	# Single res [id, title, storyline, poster_image_url, trailer_url]
	return [Movie(res[0], res[1], res[2], res[3], res[4]) for res in results]

def createMovie(title, story, poster, trailer):
	cursor = getDBCursor()
	cursor.execute('''
		INSERT INTO movies (title,story,poster,trailer) VALUES (?,?,?,?)
	''', (title,story,poster,trailer))
	id = cursor.lastrowid
	database.commit()
	cursor.close()
	return id

def updateMovie(id, title, story, poster, trailer):
	cursor = getDBCursor()
	cursor.execute('''
		UPDATE movies SET title = ?, story = ?, poster = ?, trailer = ? 
		WHERE id = ? 
	''', (title,story,poster,trailer,id))
	database.commit()
	cursor.close()

def deleteMovie(id):
	cursor = getDBCursor()
	cursor.execute('''DELETE FROM movies WHERE id = ?''', (id,))
	database.commit()
	cursor.close()