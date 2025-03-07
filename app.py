from flask import Flask, request, render_template, redirect, url_for
from storage.storage_json import Storage


app = Flask(__name__)
blog_storage = Storage('data/data.json')
posts = blog_storage.get_posts()


@app.route('/')
def index():

    """Renders the main page"""

    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():

    """
    If reqeust has method GET, renders the add page where user cand fill out the form.
    If reqeust has method POST, gets sent over data and adds them to the database.
    """

    if request.method == 'POST':
        author = request.form.get('author', None)
        title = request.form.get('title', None)
        content = request.form.get('content', None)
        if author and title and content:
            blog_storage.add_post(posts, author, title, content)
            return redirect(url_for('index'))
        else:
            raise Exception('Impossible to add the user')
    return render_template('add.html')


@app.route('/delete/<post_id>')
def delete(post_id):

    """Deletes the post from the database and redirects to the main page"""

    post_id = int(post_id)
    blog_storage.delete_post(posts, post_id)
    return redirect(url_for('index'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):

    """
    If reqeust has method GET, renders the update page where user cand edit entered data in the form.
    If reqeust has method POST, gets sent over data and rewrites the in the database.
    """

    post_id = int(post_id)
    post = blog_storage.get_post_by_id(posts, post_id)
    if request.method == 'POST':
        author = request.form.get('author', None)
        title = request.form.get('title', None)
        content = request.form.get('content', None)
        if author and title and content:
            blog_storage.update_post(posts, post_id, author, title, content)
            return redirect(url_for('index'))
        else:
            raise Exception('Impossible to add the user')
    return render_template('update.html', post=post)


@app.route('/like/<post_id>')
def like(post_id):

    """
    If like button is not pressed, increases the likes amount in the database.
    If like button is pressed, decreases the likes amount in the database.
    Redirects to the main page
    """

    post_id = int(post_id)
    blog_storage.like_post(posts, post_id)
    return redirect(url_for('index'))


if __name__ == '__main__' and blog_storage and posts:
    app.run(port=5001, debug=True)