# Homework 4, Problem 5: Comment Board

## Install and run

From a terminal, change into the `p5` folder and create a virtual environment:

```sh
cd p5
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. Open <http://127.0.0.1:5000/> in a browser. Press Ctrl+C in the terminal to stop the server. The built-in debug server and default secret key are intended for local development only; set a unique `SECRET_KEY` environment variable and use a production server for deployment.

## Test the application

1. Enter your name and a comment containing a hashtag, such as `Learning #Python is fun!`, and select **Post comment**. The comment should appear in the table with its author, date, time, and hashtag.
2. Refresh the page: the comment should remain, and your name should still appear in the form in the same browser session. Add another comment to check the table.
3. Select **Search** and try an author, words from a comment, or a hashtag (with or without `#`). Searches ignore capitalization; when multiple fields are supplied, all must match. Each entered word must appear in the comment. An empty search shows a prompt.
4. Stop and restart the app: saved comments should still be visible. They are stored in `comments.csv` beside `app.py`; deleting that file removes the saved comments.
