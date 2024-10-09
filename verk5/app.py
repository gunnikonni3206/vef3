from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_ckeditor import CKEditor, CKEditorField
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')  # Replace with a strong secret key
ckeditor = CKEditor(app)

# Admin credentials (set via environment variables for security)
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '123456')

def load_posts():
    if os.path.exists('blogs.json'):
        with open('blogs.json', 'r') as f:
            return json.load(f)
    return []

def save_posts(blogs):
    with open('blogs.json', 'w') as f:
        json.dump(blogs, f, indent=4)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

def get_random_dog_image():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    if response.status_code == 200:
        return response.json().get('message')
    return None

@app.route('/')
def index():
    blogs = load_posts()
    blogs = sorted(blogs, key=lambda x: x['date'], reverse=True)
    dog_image_url = get_random_dog_image()
    page = request.args.get('page', 1, type=int)
    per_page = 6
    total = len(blogs)
    start = (page - 1) * per_page
    end = start + per_page
    pagination_blogs = blogs[start:end]
    return render_template('index.html', blogs=pagination_blogs, page=page, total=total, per_page=per_page, dog_image_url=dog_image_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['user'] = email
            flash('You have successfully logged in.', 'success')
            return redirect(url_for('index')) 
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user' not in session:
        flash('Please log in to access the admin dashboard.', 'warning')
        return redirect(url_for('login'))
    form = BlogForm()
    if form.validate_on_submit():
        blogs = load_posts()
        new_blog = {
            'title': form.title.data,
            'content': form.content.data,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'author': session['user'],
            'image': request.form.get('image_url')
        }
        blogs.append(new_blog)
        save_posts(blogs)
        flash('New blog post created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    blogs = load_posts()
    return render_template('admin_dashboard.html', form=form, blogs=blogs)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_blog(index):
    if 'user' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    blogs = load_posts()
    if index >= len(blogs) or index < 0:
        flash('Blog post not found.', 'danger')
        return redirect(url_for('admin_dashboard'))
    blog = blogs[index]
    form = BlogForm()
    if form.validate_on_submit():
        blogs[index]['title'] = form.title.data
        blogs[index]['content'] = form.content.data
        blogs[index]['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        blogs[index]['author'] = session['user']
        blogs[index]['image'] = request.form.get('image_url')
        save_posts(blogs)
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    form.title.data = blog['title']
    form.content.data = blog['content']
    return render_template('edit_blog.html', form=form, index=index)

@app.route('/delete/<int:index>', methods=['POST'])
def delete_blog(index):
    if 'user' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    blogs = load_posts()
    if index >= len(blogs) or index < 0:
        flash('Blog post not found.', 'danger')
        return redirect(url_for('admin_dashboard'))
    blogs.pop(index)
    save_posts(blogs)
    flash('Blog post deleted successfully.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message="Internal Server Error"), 500

if __name__ == '__main__':
    app.run(debug=True)
