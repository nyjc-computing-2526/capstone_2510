"""
Provides a render_template function which embeds session
info into the render context.
"""

from flask import render_template as old_render
from flask import session

def render_template(*args, **kwargs):
    if "name" in session:
        user_name = session["name"]
    else:
        user_name = None
    return old_render(*args, user_name = user_name, **kwargs)