import os
from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename

from . import app, db
from .forms import ReviewFrom, FilmFrom
from .models import Movie, Review


@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('index.html',
                           movies=movies)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = FilmFrom()
    if form.validate_on_submit():
        film = Movie()
        film.title = form.title.data
        film.description = form.description.data
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            film.image = form.image.data.filename
        db.session.add(film)
        db.session.commit()
        return redirect(url_for('movie_detail', id=film.id))
    return render_template('add_movie.html',
                           form=form)


@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie_detail(id: int):
    movie = Movie.query.get(id)
    if movie.reviews:
        avg_score = round(sum(review.score \
            for review in movie.reviews) / 
                          len(movie.reviews), 2)
    else:
        avg_score = 0
    form = ReviewFrom(score=10)
    if form.validate_on_submit():
        review = Review()
        review.name = form.name.data
        review.text = form.text.data
        review.score = form.score.data
        review.movie_id = movie.id
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movie_detail', id=movie.id))
    return render_template('movie.html',
                           movie=movie,
                           avg_score=avg_score,
                           form=form)
