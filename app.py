from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    with open("blog_posts.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)

    return blog_posts


def save_posts(blog_posts):
    with open("blog_posts.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, ensure_ascii=False, indent=4)


@app.route('/')
def index():
    blog_posts = load_posts()

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        blog_posts = load_posts()

        new_post = {
            "id": max([post["id"] for post in blog_posts], default=0) + 1,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }

        blog_posts.append(new_post)

        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()

    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    save_posts(blog_posts)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run("127.0.0.1", port=3000, debug=True)
