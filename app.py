"""
The main entry point for the application.
"""
from flask import Flask, render_template as renderTemplate

app = Flask(__name__)


@app.route("/")
def helloWorld() -> str:
    """
    Renders the index.html template.

    Returns:
        The rendered index.html template.
    """
    return renderTemplate("index.html")


if __name__ == "__main__":
    app.run()
