import logging

from flask import Flask, render_template, request

from viewmodel import ViewModel

app = Flask(__name__)
app.debug = True

@app.route('/main', methods=['GET', 'POST'])
def form():
    view_model = ViewModel.make_from_request(request)
    return render_template('main.html', view_model=view_model)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
