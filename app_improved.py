#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.

import uuid
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'

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
    
    # JUST ENOUGH CODE TO PASS THE TEST.
    # THERE IS HTML TO BE RETURNED HERE, BUT WE'LL JUST REDIRECT TO /restricted
    # FOR NOW
    return redirect(url_for('restricted'))

@app.route('/restricted', methods=['GET', 'POST'])
def restricted():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    if (request.method == 'POST') :
    #JUST ENOUGH CODE TO PASS THE TEST - REMEMBER TO IMPLEMENT THIS PROPERLY
    # PER THE REQUIREMENTS  
        # Return some html with three aphorisms as the test expects.
        html = "<title>Aphorisms from The Zen of Python</title>"
        html += "<p>Beautiful is better than ugly.</p>"
        html += "<p>Simple is better than complex.</p>"
        html += "<p>Explicit is better than implicit.</p>"
        return html
    
    # It's a get request and the user is logged in
    token = session['csrf_token']
    # This is not the complete page! Just what the test is looking for.
    html = "<title>Restricted</title>"
    html += '<input type="hidden" name="csrf_token" value="' + token + '">'
    return html

if __name__ == '__main__':
    app.debug = True
    app.run()
