"""
The main entry point for the application.
"""
# Standard library imports
from pathlib import Path

# External imports
from flask import Flask, render_template as renderTemplate, request

# Internal imports
from internals import Database, Config, createLogger

config: Config = Config(Path("ServerData/config.json"))
database: Database = Database(Path("ServerData/database.db"))

app = Flask(__name__)


@app.route("/")
def helloWorld() -> str:
    """
    Renders the index.html template.

    Returns:
        The rendered index.html template.
    """
    return renderTemplate("index.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """
    Depending on the request method, renders the login.html template or logs the user in.

    Returns:
        The rendered login.html template.
    """
    if request.method == "POST":
        # Log the user in
        pass

    # Render the login page
    return renderTemplate("login.html")


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    """
    Depending on the request method, renders the register.html template or registers the user.

    Returns:
        The rendered register.html template.
    """
    if request.method == "POST":
        # Register the user
        pass

    # Render the register page
    return renderTemplate("register.html")


if __name__ == "__main__":
    app.run()
