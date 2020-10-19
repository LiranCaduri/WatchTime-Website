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
        
    return render_template('search.html', data= json.loads(response.content), name=result)

@app.route('/show/<string:id>') # figure that out 
def show_page():
    # mabye try pass param in url_for on frontend with key and val
    pass

if __name__ == '__main__':
    app.run(debug=True)
