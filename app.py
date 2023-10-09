"""
The main entry point for the application.
"""
# Standard library imports
from pathlib import Path
from secrets import token_urlsafe
from logging import StreamHandler, FileHandler, getLogger
from sys import stdout
from datetime import datetime

# External imports
from flask import Flask, render_template as renderTemplate, request, session, redirect, url_for, Response
from flask_session import Session
from redis import from_url

# Internal imports
from internals import Database, Config, createLogger, RequestFormatter

config: Config = Config(Path("ServerData/config.json"))
database: Database = Database(config, Path("ServerData/database.db"))

# Set up the flask app
app = Flask(__name__)

# TODO: Get all of this garbage working
# # Ensure App Logs directory exists
# Path("Logs/App").mkdir(parents=True, exist_ok=True)
#
# # Create app logger handlers
# streamHandler: StreamHandler = StreamHandler(stdout)
# streamHandler.setFormatter(RequestFormatter("[%(asctime)s] [APP] [%(levelname)s] [%(remoteAddr)s] %(message)s"))  # The
# # APP being the logger name is a workaround, because logging is stupid
#
# fileHandler: FileHandler = FileHandler(Path(f"Logs/App/AppLog{datetime.now().strftime('%d.%m.%Y')}.log"))
#
# # Clear the app logger handlers
# app.logger.handlers.clear()
#
# # Add the app logger handlers
# app.logger.addHandler(streamHandler)
# app.logger.addHandler(fileHandler)
#
# # Do the same for the werkzeug logger
# logger = getLogger("werkzeug")
# logger.handlers.clear()
#
# logger.addHandler(streamHandler)
# logger.addHandler(fileHandler)

# Set the secret key
app.secret_key = config.Server.SecretKey

# Configure the app
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

# Set up the redis session
app.config["REDIS_HOST"] = "localhost"
app.config["REDIS_PORT"] = 6379
app.config["REDIS_PASSWORD"] = config.Server.RedisPassword

# Set up the session
serverSession = Session(app)


@app.route("/")
def index() -> str:
    """
    Renders the index.html template.

    Returns:
        The rendered index.html template.
    """

    return renderTemplate("index.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """
    Depending on the request method, renders the login.html template or logs the user in.

    Returns:
        The rendered login.html template.
    """
    # Log the user in
    if request.method == "POST":
        # Get the form data
        email: str = request.form["email"]
        password: str = request.form["password"]

        # Check if the user exists
        if not database.checkUserEmailExists(email):
            # Render the login page with an error
            return renderTemplate("login.html", error="User does not exist.")

        # Check if the password is correct
        if not database.attemptLogin(email, password):
            # Remove the password from memory
            password = None  # type: ignore  # Ignore the type error for deleting
            del password

            # Render the login page with an error
            return renderTemplate("login.html", error="Incorrect password.")

        # Remove the password from memory
        password = None  # type: ignore  # Ignore the type error for deleting
        del password

        # Set the session variables
        # session["email"] = email
        # session["userId"] = database.getUserId(email)

        # Redirect the user to the index page
        print(session.values())
        return redirect(url_for("index"))

    # Render the login page
    return renderTemplate("login.html")


@app.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    """
    Depending on the request method, renders the register.html template or registers the user.

    Returns:
        The rendered register.html template.
    """
    # Register the user
    if request.method == "POST":
        # Get the form data
        firstName: str = request.form["firstName"]
        lastName: str = request.form["lastName"]
        email: str = request.form["email"]
        password: str = request.form["password"]
        confirmPassword: str = request.form["confirmPassword"]

        # Check if the passwords match
        if password != confirmPassword:
            # Render the register page with an error
            return renderTemplate("register.html", error="Passwords do not match.")

        # Remove the confirmation password from memory
        del confirmPassword

        # Check if the email is already in use
        if database.checkUserEmailExists(email):
            # Render the register page with an error
            return renderTemplate("register.html", error="Email already in use.")

        # Create the user
        database.addUser(firstName, lastName, email, password)

        # Remove the password from memory
        password = None  # type: ignore  # Ignore the type error for deleting
        del password

        # Redirect the user to the login page
        return redirect(url_for("login"))

    # Render the register page
    return renderTemplate("register.html")


if __name__ == "__main__":
    app.run()
