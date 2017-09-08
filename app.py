import functools
import enum
from typing import Callable, Optional
import os

from flask import Flask, redirect, render_template, session, url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.jinja_env.auto_reload = True  # Don't cache templates


def register_place(place_name: str):
    """ Register a place to be in a game place.
        Registered places are recorded in history.

        We use `str` as an identifier because it is JSON serializable
        (unlike enum)
    """
    def decorator(f: Callable):
        @functools.wraps(f)
        def decorated_f(*args, **kwargs):
            session['history'].append(place_name)
            session.modified = True
            return f(*args, **kwargs)

        return decorated_f
    return decorator

def current_place() -> Optional[str]:
    """ Current place that player is in. """
    if not session['history']:
        return None
    return session['history'][-1]


def last_place() -> Optional[str]:
    """ Last place that player visited """
    if len(session['history']) < 2:
        return None
    return session['history'][-2]

@app.before_request
def reset():
    """ If session history does not exist, reset game """
    if session.get('history') is None:
        # Basic session setup
        session.permanent = True
        session['history'] = []
        return redirect(url_for('index'))


@app.route('/')
def redirect_to_index():
    return redirect(url_for('index'))

@app.route('/index.htm')
def index():
    return render_template('index.html')


@app.route('/frontdoor.htm')
@register_place('frontdoor')
def frontdoor():
    if last_place() == 'secondfloor':
        return 'death'
    return render_template('frontdoor.html')


@app.route('/firstfloor.htm')
@register_place('firstfloor')
def firstfloor():
    return render_template('firstfloor.html')


@app.route('/secondfloor.htm')
@register_place('secondfloor')
def secondfloor():
    return render_template('secondfloor.html')
