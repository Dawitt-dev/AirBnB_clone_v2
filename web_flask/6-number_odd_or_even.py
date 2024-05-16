#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """Displays 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def display_c(text):
    """Displays 'C ' followed by the value of the text variable"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python(text):
    """Displays 'Python ' followed by the value of the text variable"""
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def display_number(n):
    """Displays '<n> is a number' only if n is an integer"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def display_number_template(n):
    """Displays an HTML 'Number: n' if n is an integer"""
    if isinstance(n, int):
        return render_template('6-number.html', n=n)
    else:
        return 'Not Found', 404


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def display_number_odd_or_even(n):
    """Displays an HTML containiing 'Number: n is even|odd' if n is an int"""
    if isinstance(n, int):
        return render_template('6-number_odd_or_even.html',
                               n=n, odd_even='odd' if n % 2 != 0 else 'even')
    else:
        return 'Not Found', 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)