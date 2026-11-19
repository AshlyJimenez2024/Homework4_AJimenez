"""A small Flask comment board that stores its comments in a CSV file."""

import csv
import os
import re
from datetime import datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
# Set SECRET_KEY in the environment when deploying the application.
app.secret_key = os.environ.get("SECRET_KEY", "homework4-local-development-key")
CSV_FILE = Path(__file__).resolve().parent / "comments.csv"
FIELDS = ["author", "date", "time", "comment", "hashtags"]
HASHTAG_PATTERN = re.compile(r"(?<!\w)#[\w]+")


def read_comments():
    """Return saved comments, newest first."""
    if not CSV_FILE.exists():
        return []
    with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(reversed(list(csv.DictReader(file))))


def save_comment(author, comment):
    now = datetime.now()
    hashtags = list(dict.fromkeys(HASHTAG_PATTERN.findall(comment)))
    row = {
        "author": author,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "comment": comment,
        "hashtags": " ".join(hashtags),
    }
    new_file = not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0
    with CSV_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        author = request.form.get("author", "").strip()
        comment = request.form.get("comment", "").strip()
        if author:
            session["username"] = author
        if not author or not comment:
            error = "Please enter your name and a comment."
        else:
            save_comment(author, comment)
            return redirect(url_for("index"))
    return render_template(
        "index.html", comments=read_comments(), error=error,
        username=session.get("username", ""),
        comment=request.form.get("comment", ""),
    )


@app.route("/search")
def search():
    author = request.args.get("author", "").strip()
    words = request.args.get("words", "").strip()
    hashtag = request.args.get("hashtag", "").strip().lstrip("#")
    results = []
    if author or words or hashtag:
        for item in read_comments():
            tags = {tag[1:].casefold() for tag in item["hashtags"].split()}
            if (author.casefold() in item["author"].casefold()
                    and all(word.casefold() in item["comment"].casefold()
                            for word in words.split())
                    and (not hashtag or hashtag.casefold() in tags)):
                results.append(item)
    return render_template("search.html", comments=results, author=author,
                           words=words, hashtag=hashtag)


if __name__ == "__main__":
    app.run(debug=True)
