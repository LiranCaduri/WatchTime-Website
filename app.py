from flask import Flask, render_template, request, redirect, url_for
import requests
import json

genres_list = [
        "Comedy",
        "Fantasy",
        "Crime",
        "Drama",
        "Music",
        "Adventure",
        "History",
        "Thriller",
        "Anime",
        "Family",
        "Mystery",
        "Action",
        "Romance",
        "War",
        "Western",
        "Horror",
        "Supernatural"
    ]

app = Flask(__name__)

@app.route('/')
@app.route('/<int:page>')
def index(page=0):
    try:
        response = requests.get(f'http://api.tvmaze.com/shows?page={page}')
    except:
        #frontend will print out or show 404 page
        data = None
    else:
        data= json.loads(response.content)
    return render_template('index.html', data=data, category="all", genres=genres_list, page=page)


@app.route('/search', methods = ['POST'])
def search():
   
    result = request.form['show']
    try:
        response = requests.get(f'http://api.tvmaze.com/search/shows?q={result}')
    except:
        #frontend will print out
        data = None
    else:
        data= json.loads(response.content)

    return render_template('search.html', data=data, name=result)


@app.route('/show/<int:show_id>')
def show_page(show_id):
    url = f'http://api.tvmaze.com/shows/{show_id}'

    try:
        response = requests.get(f'{url}?embed[]=cast')
        images_data = requests.get(f'{url}/images')
    except:
        data = None
        images_reversed=None
    else:
        data= json.loads(response.content)
        images_data = json.loads(images_data.content)
        images_reversed =(list(reversed(images_data)))

    background = None
    if images_reversed:
        for img in images_reversed:
            if img['type'] == 'background':
                background = img

    actors_without_duplicates = set()
    for obj in data['_embedded']['cast']:
        actors_without_duplicates.add((obj["person"]["name"], obj["person"]["image"]["medium"]))

    return render_template('show_page.html', data=data, cast=list(actors_without_duplicates), background=background)


@app.route('/genre/<string:genre>/<int:page>')
def genre_filter(genre, page=0):
    if genre.lower() == 'all':
        return redirect(url_for('index'))
    try:
        response = requests.get(f'http://api.tvmaze.com/shows?page={page}')
    except:
        data= None
    else:
        data = json.loads(response.content)

    filtered = []
    if data:
        for obj in data:
            for g in obj['genres']:
                if g.lower() == genre.lower():
                    filtered.append(obj)

    return render_template('genreFooterComponent.html', data=filtered , category=genre.title(),genre=genre, genres=genres_list, page=page)

@app.route('/<int:rating>/<int:page>')
def rating_filter(rating, page):
    try:
        response = requests.get(f'http://api.tvmaze.com/shows?page={page}')
    except:
        data= None
    else:
        data = json.loads(response.content)

    filtered = []
    if data:
        for obj in data:
            r = obj['rating']['average']
            if rating == 0:
                if r is None:
                    filtered.append(obj)
            if not(r is None):
                if rating >= r < rating + 1:
                    filtered.append(obj)
                

    
    return render_template('raitingFooterComponent.html', data=filtered, rating=rating, category=f"rating {rating}", page=page)


@app.errorhandler(404)
def not_found(e):
    return render_template('404page.html'), 404


if __name__ == '__main__':
    app.run()
