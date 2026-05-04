from flask import request, render_template, redirect, session
from app_obj import app

@app.route("/")
def landing():
    return render_template('landing.html')

@app.route("/privacy_policy")
def privacy():
    return render_template('privacy.html') #privacy.html not written yet

@app.route("/contact_us")
def contact():
    return render_template('contact.html')
