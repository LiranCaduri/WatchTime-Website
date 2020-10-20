from flask import Flask, render_template, request
import requests
import json

# TODO - add try catch to all request
# TODO - make 404 page design
# TODO - fix search to match smartphones
# TODO - make filters by data manipulation (needed making by hand)
# TODO - show text when there is no result
# TODO - add Cast
# TODO - use background photo for show page (http://api.tvmaze.com/shows/4/images)

app = Flask(__name__)

@app.route('/')
def index():
    #http://api.tvmaze.com/shows
    response = requests.get('http://api.tvmaze.com/shows')
    return render_template('index.html', data= json.loads(response.content), category="all")


@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        result = request.form['show']
        response = requests.get(f'http://api.tvmaze.com/search/shows?q={result}')
    return render_template('search.html', data= json.loads(response.content), name=result)


@app.route('/show/<int:show_id>')
def show_page(show_id):
    response = requests.get(f'http://api.tvmaze.com/shows/{show_id}')

    return render_template('show_page.html', data= json.loads(response.content))

if __name__ == '__main__':
    app.run(debug=True)
