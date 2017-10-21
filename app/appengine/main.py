import logging

"""
This module defines a Flask App.
"""

from flask import Flask, render_template, request

# Import web app classes.
from viewmodel import ViewModel

# Import allocation modelling classes.
from model.assayallocator import AssayAllocator
from model.experimentreporter import ExperimentReporter
from model.experimentdesign import ExperimentDesign

app = Flask(__name__)
app.debug = True

@app.route('/main', methods=['GET', 'POST'])
def form():
    # Initialise the view model for the general case of GET/POST, to reflect
    # the form inputs back in the page that is returned.
    view_model = ViewModel.initialise_from_request_form(request)

    # If we are receiving a form with fresh input parameters, then we need
    # to harvest these, use them to run an experiment, and finally update the
    # view model with the results.
    if request.method == 'POST':
        experiment_design = ExperimentDesign.make_from_html_input_form_dict(
            request.form)

        allocator = AssayAllocator(experiment_design)
        allocation = allocator.allocate()
        reporter = ExperimentReporter(allocation, experiment_design)
        view_model.populate_with_experiment_results(reporter)

    return render_template('main.html', view_model=view_model)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
