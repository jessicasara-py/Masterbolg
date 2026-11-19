import json
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


def load_posts():
    """Lädt alle Blogbeiträge aus der JSON-Datei."""
    with open("blog_posts.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)

    return blog_posts


def fetch_post_by_id(post_id):
    """Sucht einen Blogbeitrag anhand seiner ID."""
    blog_posts = load_posts()

    for post in blog_posts:
        if post["id"] == post_id:
            return post

    return None


def save_posts(blog_posts):
    """Speichert alle Blogbeiträge in der JSON-Datei."""
    with open("blog_posts.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, ensure_ascii=False, indent=4)


@app.route("/")
def index():
    """Zeigt die Startseite mit allen Blogbeiträgen an."""
    blog_posts = load_posts()

    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Erstellt einen neuen Blogbeitrag."""
    if request.method == "POST":
        blog_posts = load_posts()

        new_post = {
            "id": max([post["id"] for post in blog_posts], default=0) + 1,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content"),
            "likes": 0
        }

        blog_posts.append(new_post)

        save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """Bearbeitet einen bestehenden Blogbeitrag anhand seiner ID."""
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        blog_posts = load_posts()

        for blog_post in blog_posts:
            if blog_post["id"] == post_id:
                blog_post["author"] = request.form.get("author")
                blog_post["title"] = request.form.get("title")
                blog_post["content"] = request.form.get("content")
                break

        save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    """Löscht einen Blogbeitrag anhand seiner ID."""
    blog_posts = load_posts()

    blog_posts = [
        post for post in blog_posts if post["id"] != post_id
    ]

    save_posts(blog_posts)

    return redirect(url_for("index"))


@app.route("/like/<int:post_id>")
def like(post_id):
    """Erhöht die Anzahl der Likes eines Blogbeitrags."""
    blog_posts = load_posts()

    for post in blog_posts:
        if post["id"] == post_id:
            post["likes"] = post.get("likes", 0) + 1
            break

    save_posts(blog_posts)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)
