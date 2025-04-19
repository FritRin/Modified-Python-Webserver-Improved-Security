#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.

import uuid
import secrets
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict',
)

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('u1163857', 'csc2330a3'), ('u1163857', 't12025')]:
            session['username'] = username
            session['csrf_token'] = uuid.uuid4().hex
            return redirect(url_for('index'))
    return render_template('login.html', username=username)

@app.route('/logout')
def logout():
    username = session.get('username')

    if not username:
        return redirect(url_for('login'))
    
    session.clear()

    html = "<title>Logged out</title>"
    return html

@app.route('/')
def index():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('success.html')

@app.route('/restricted', methods=['GET', 'POST'])
def restricted():
    username = session.get('username')
    #if not username:
        #return redirect(url_for('login'))
        
    # It's a get request and the user is logged in
    token = session.get('csrf_token')
    if token:
        if request.method == 'GET':
            return render_template('restricted.html')
    
    #if (request.method == 'POST') :
    #JUST ENOUGH CODE TO PASS THE TEST - REMEMBER TO IMPLEMENT THIS PROPERLY
    # PER THE REQUIREMENTS  
        # Return some html with three aphorisms as the test expects.
        #html = "<title>Aphorisms from The Zen of Python</title>"
        #html += "<p>Beautiful is better than ugly.</p>"
        #html += "<p>Simple is better than complex.</p>"
        #html += "<p>Explicit is better than implicit.</p>"
        #return html
    


if __name__ == '__main__':
    app.debug = True
    app.run()
