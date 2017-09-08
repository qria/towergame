from flask import Flask, redirect, render_template, url_for


app = Flask(__name__)
app.jinja_env.auto_reload = True  # Don't cache templates


@app.route('/')
def redirect_to_index():
	return redirect(url_for('index'))

@app.route('/index.htm')
def index():
    return render_template('index.html')


@app.route('/frontdoor.htm')
def front_door():
    return render_template('frontdoor.html')
