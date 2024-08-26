from flask import Flask, render_template

app = Flask(__name__)

blog_posts = [
    {"id": 0, "title": "Hvað er Jinja2", "content": "Jinja2 er templatekerfi ...", "picture": "img1.JPG", "author": "Gunnar", "category": "Jinja2", "date_posted": "20.08.2024"},
    {"id": 1, "title": "Hvað er Pico", "content": "Pico er CSS safn ...", "picture": "img2.JPG", "author": "Karl", "category": "CSS", "date_posted": "21.08.2024"},
    {"id": 2, "title": "Hvað er Flask", "content": "Flask er microframework ...", "picture": "img3.JPG", "author": "John Doe", "category": "Flask", "date_posted": "23.08.2024"}
]

@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/post/<int:id>')
def post(id):
    post = next((post for post in blog_posts if post["id"] == id), None)
    return render_template('blogpost.html', post=post)

@app.route('/category/<category_name>')
def category(category_name):
    category_posts = [post for post in blog_posts if post["category"].lower() == category_name.lower()]
    return render_template('category.html', posts=category_posts, category_name=category_name)

if __name__ == "__main__":
    app.run(debug=True)



