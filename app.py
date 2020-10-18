from flask import Flask, render_template, request
import requests
import json


# TODO - add try catch to all request
# TODO - make 404 page design

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
        # f'http://api.tvmaze.com/search/shows?q={result}'
        response = requests.get(f'http://api.tvmaze.com/search/shows?q={result}')
        # print(json.loads(response.content))
    return render_template('search.html', data= json.loads(response.content))

if __name__ == '__main__':
    app.run(debug=True)
