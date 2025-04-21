#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.

import uuid
import secrets
import random, socket, zen_utils
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

    return render_template('logout.html')

@app.route('/')
def index():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('success.html')

@app.route('/restricted', methods=['GET', 'POST'])
def restricted():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
        
    # It's a get request and the user is logged in
    token = session.get('csrf_token')
    if token:
        if request.method == 'GET':
            return render_template('restricted.html', csrf_token = token)
    
    if (request.method == 'POST'):
        if token:
            aphorisms = client(('127.0.0.1', 1060))
            return render_template('aphorisms.html', aphorisms = aphorisms)

def client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    aphorisms = list(zen_utils.aphorisms)
    results = []
    for aphorism in random.sample(aphorisms, 3):
        sock.sendall(aphorism)
        response = aphorism.decode().strip().replace('?', ' ') + ((zen_utils.recv_until(sock, b'.')).decode().lower()).strip()
        results.append(response)
    
    sock.close()
    return results


if __name__ == '__main__':
    app.debug = True
    app.run()
