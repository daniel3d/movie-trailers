# -*- coding: utf-8 -*-
"""Media module for movie-trailers.

Module to showcase our code for Udacity Full Stack Web Developer Nanodegree
the module is build with best standards as suggested by the
Udacity reviwer PEP8 and PEP257

Todo:
    * Try implementing the `class Movie` with eloquent 0.5

"""
import sqlite3

database = sqlite3.connect('movies.db')
"""Curent connection to the database"""


class Movie():
    """Persistent database class with basic CRUD."""

    def __init__(self, title, story, poster, trailer, id=0):
        """Initialise movie in to memory.

        Args:
        title	(str): The movie titles.
        story	(str): The movie Description.
        poster	(str): The movie poster image url.
        trailer (str): The movie trailer youtube id.
        id		(int, optional): The movie database id

        """
        self.id = id
        self.title = title
        self.story = story
        self.poster = poster
        self.trailer = trailer

    def save(self):
        """Upate or create database record."""
        if self.id:  # if we have id let update
            cursor = database.cursor()
            cursor.execute('''
                UPDATE movies SET title = ?, story = ?, poster = ?, trailer = ?
                WHERE id = ?
            ''', (self.title, self.story, self.poster, self.trailer, self.id))
            database.commit()
            cursor.close()
            return self
        else:  # if we are trying to save new one let create it first
            return self.create()

    def create(self):
        """Create new database record."""
        cursor = database.cursor()
        cursor.execute('''
            INSERT INTO movies (title,story,poster,trailer) VALUES (?,?,?,?)
        ''', (self.title, self.story, self.poster, self.trailer))
        self.id = cursor.lastrowid
        database.commit()
        cursor.close()
        return self

    def delete(self):
        """Remove database record."""
        cursor = database.cursor()
        cursor.execute('''DELETE FROM movies WHERE id = ?''', (self.id,))
        database.commit()
        cursor.close()


def getAllMovies():
    """Get all database records."""
    cursor = database.cursor()
    cursor.execute('''SELECT * FROM movies''')
    results = cursor.fetchall()
    cursor.close()
    # [(id, title, storyline, poster, trailer_url)]
    return [Movie(r[1], r[2], r[3], r[4], r[0]) for r in results]


def getMovieById(id):
    """Seach for movie with `id` stored in the database.

    Args:
    id (int): The movie `id` we are looking for

    Returns:
    obj: If we have a match will return the instance of the Movie class pre
        loaded with the (`id`, `title`, `story`, `poster`, `trailer`)
    bool: False if we dont have a match

    """
    cursor = database.cursor()
    cursor.execute('''SELECT * FROM movies WHERE id = ?''', (id,))
    r = cursor.fetchall()
    cursor.close()
    if len(r) == 1:
        # [(id, title, storyline, poster_image_url, trailer_url)]
        return Movie(r[0][1], r[0][2], r[0][3], r[0][4], r[0][0])
    else:
        return False
