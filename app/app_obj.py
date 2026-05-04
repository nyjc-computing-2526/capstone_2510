"""
Shared app object.
"""

from flask import Flask

app = Flask(__name__)
app.secret_key = "2510_xx_xx"

