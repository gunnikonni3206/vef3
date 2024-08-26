from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_ckeditor import CKEditor, CKEditorField
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
ckeditor = CKEditor(app)

# Placeholder data structure to store blog posts
blog_posts = []

# WTForms for login and creating a blog post
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'dummy@mail.com' and form.password.data == '123456':
            session['user'] = form.email.data
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Admin route
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    form = PostForm()
    if form.validate_on_submit():
        post = {
            "title": form.title.data,
            "content": form.content.data,
            "author": form.author.data,
            "date_posted": datetime.datetime.now().strftime('%Y-%m-%d')
        }
        blog_posts.append(post)
        flash('Post created successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('admin.html', form=form)

# Homepage route
@app.route('/')
def index():
    sorted_posts = sorted(blog_posts, key=lambda x: x['date_posted'], reverse=True)
    return render_template('index.html', posts=sorted_posts)

if __name__ == "__main__":
    app.run(debug=True)
