from flask import Flask, render_template, redirect, url_for, request, flash, session
import urllib.request, json, ssl
import certifi
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

certifi_context = ssl.create_default_context(cafile=certifi.where())

@app.route('/')
def index():
    api_key = app.config['API_KEY']
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&page=1"
    
    with urllib.request.urlopen(url, context=certifi_context) as response:
        movies = json.loads(response.read())
    
    return render_template('index.html', movies=movies['results'])

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    api_key = app.config['API_KEY']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    
    with urllib.request.urlopen(url, context=certifi_context) as response:
        movie = json.loads(response.read())
    
    return render_template('movie_details.html', movie=movie)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'dummy@mail.com' and password == '123456':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        flash('Post added successfully')
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
