from flask import Flask, render_template, url_for
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    #http://api.tvmaze.com/shows
    respones = requests.get('http://api.tvmaze.com/shows')
    print(len(json.loads(respones.content)))
    return render_template('index.html', title="WatchTime", data= json.loads(respones.content), category="all")
    

app.run(debug=True)