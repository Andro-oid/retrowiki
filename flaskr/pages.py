from flask import render_template, redirect, url_for
from flask import request
from flaskr.backend import Backend
import hashlib


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

    # TODO(Project 1): Implement additional roautes according to the project requirements.
    @app.route("/pages", methods=["POST"])
    def pages():
        nonlocal loggedIn
        nonlocal sessionUserName
        pages = db.get_all_page_names()
        return render_template("pages.html", listPages = pages)
        
    @app.route("/about")
    def about():
        nonlocal loggedIn
        nonlocal sessionUserName
        
        # print("==========================================================================")
        imageManuelMares = db.get_image("ManuelMares")
        # print(imageManuelMares + "========================================================")
        return render_template("about.html", img_Manuel = imageManuelMares)
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
                return render_template("login.html", error =True)
        else:
            return render_template("login.html", error =False)

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
                return render_template("signup.html", error =True)
        else:
            return render_template("signup.html", error =True)

    @app.route("/upload", methods = ["GET", "POST"])
    def upload():
        nonlocal loggedIn
        nonlocal sessionUserName
        return render_template("upload.html")
