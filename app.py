from flask import Flask, render_template, request, redirect, url_for
import requests
import json

# TODO - add try catch to all request
# TODO - make 404 page design
# TODO - fix search design to match smartphones
# TODO - make filters by data manipulation (needed making by hand) (filters: by rating out of 10, by actress, by genre ...)
# TODO - show text when there is no result
# TODO - add Cast
# TODO - implement figur 

genres_list = [
        "Comedy",
        "Fantasy",
        "Crime",
        "Drama",
        "Music",
        "Adventure",
        "History",
        "Thriller",
        "Animation",
        "Family",
        "Mystery",
        "Biography",
        "Action",
        "Film-Noir",
        "Romance",
        "Sci-Fi",
        "War",
        "Western",
        "Horror",
        "Musical",
        "Sport"
    ]

app = Flask(__name__)

@app.route('/')
@app.route('/<int:page>')
def index(page=0):
    #http://api.tvmaze.com/shows
    response = requests.get(f'http://api.tvmaze.com/shows?page={page}')
    return render_template('index.html', data= json.loads(response.content), category="all", genres=genres_list)


@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        result = request.form['show']
        response = requests.get(f'http://api.tvmaze.com/search/shows?q={result}')
    return render_template('search.html', data= json.loads(response.content), name=result)


@app.route('/show/<int:show_id>')
def show_page(show_id):
    url = f'http://api.tvmaze.com/shows/{show_id}'
    response = requests.get(url)

    images_data = requests.get(f'{url}/images')
    images_data = json.loads(images_data.content)
    images_reversed =(list(reversed(images_data)))

    background = None
    for img in images_reversed:
        if img['type'] == 'background':
            background = img

    return render_template('show_page.html', data= json.loads(response.content), background=background)


@app.route('/genre/<string:genre>/<int:page>')
@app.route('/genre/<string:genre>')
def genre_filter(genre, page=0):
    
    if genre.lower() == 'all':
        return redirect(url_for('index'))

    response = requests.get(f'http://api.tvmaze.com/shows?page={page}')
    data = json.loads(response.content)

    filtered = []

    for obj in data:
        for g in obj['genres']:
            if g.lower() == genre.lower():
                filtered.append(obj)

    return render_template('index.html', data=filtered , category=genre.title(), genres=genres_list)


if __name__ == '__main__':
    app.run(debug=True)
