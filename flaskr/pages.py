from flask import render_template, redirect, url_for
from flask import request
from flaskr.backend import Backend
import hashlib
from google.cloud import storage
from .wikimusic import get_wikipedia_articles, get_iframe_spotify_songs


def make_endpoints(app):
    loggedIn = False
    db = Backend()
    sessionUserName = ""

    @app.context_processor
    def inject_now():
        """
        This variables are known are send to all templated when used. 
        Their value cannot be modified. Instead, we use a condition to decide
        what value to send.
        """
        if loggedIn:
            return {'loggeda': True, "userName": sessionUserName}
        else:
            return {'loggeda': False, "userName": ""}

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/home", methods=["GET"])
    @app.route("/", methods=["GET"])
    def home():
        nonlocal loggedIn
        nonlocal sessionUserName
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("home.html")

    @app.route("/<usr>")
    def user(usr, pwd):
        nonlocal loggedIn
        nonlocal sessionUserName
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return f"<h1>{usr}</h1> <h2>{pwd}<h2>"

    #uses backend to obtain list of wiki content, sends that list when rendering pages.html
    @app.route("/pages", methods=["GET"])
    def pages(page=None):
        nonlocal loggedIn
        nonlocal sessionUserName
        pages = db.get_all_page_names()
        return render_template("pages.html", listPages=pages, page=page)

    #uses backend to obtain content of a certain page, sends the content when rendering pages.html
    @app.route("/pages/<path>", methods=["GET"])
    def current_page(path):
        nonlocal loggedIn
        nonlocal sessionUserName
        page = db.get_wiki_page(path)
        return render_template("pages.html", listPages=None, page=page)

    @app.route("/about")
    def about():
        nonlocal loggedIn
        nonlocal sessionUserName
        return render_template("about.html")

    @app.route("/logout")
    def logout():
        nonlocal loggedIn
        nonlocal sessionUserName
        loggedIn = False
        return redirect(url_for('home'))

    @app.route("/login", methods=["POST", "GET"])
    def login():
        nonlocal loggedIn
        nonlocal sessionUserName
        if request.method == "POST":
            user = request.form["nm"]
            password = hashlib.blake2b(request.form["pwd"].encode()).hexdigest()
            if db.sign_in(user, password):
                loggedIn = True
                sessionUserName = user
                return redirect(url_for('home'))
            else:
                return render_template("login.html", error=True)
        else:
            return render_template("login.html", error=False)

    @app.route("/signup", methods=["POST", "GET"])
    def signup():
        nonlocal loggedIn
        nonlocal sessionUserName
        if request.method == "POST":
            user = request.form["nm"]
            password = hashlib.blake2b(request.form["pwd"].encode()).hexdigest()
            if db.sign_up(user, password):
                loggedIn = True
                sessionUserName = user
                return redirect(url_for('home'))
            else:
                return render_template("signup.html", error=True)
        else:
            return render_template("signup.html", error=False)

    @app.route("/upload", methods=["GET", "POST"])
    def upload():
        client = storage.Client()
        if request.method == "POST":
            file = request.files["fileUpload"]
            filename = file.filename
            blob = client.bucket("group_wiki_content").blob(filename)
            blob.upload_from_file(file)
            return render_template("upload.html",
                                   message="File uploaded successfully.")
        return render_template("upload.html")

    @app.route("/wikimusic", methods=["GET", "POST"])
    def wikiAPIRequest():
        if request.method == "POST":
            songname = request.form["songname"]
            artist = request.form["artist"]
            if songname == "" or artist == "":
                return render_template("wikimusic_notfound.html")

            iframes = get_iframe_spotify_songs(songname, artist)
            articles = get_wikipedia_articles(songname + " " + artist)

            if len(articles) == 0:
                return render_template("wikimusic_notfound.html")
            else:
                return render_template("WikiMusicAnswer.html",
                                       articles=articles,
                                       iframes_spotify=iframes)
        else:
            return render_template("WikiMusicStart.html")
