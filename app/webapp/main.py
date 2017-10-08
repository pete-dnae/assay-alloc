from flask import Flask, render_template

app = Flask('assay-allocation-app', 
        static_folder='/app/static',
        template_folder='/app/templates')

@app.route('/')
def hello(name=None):
    return render_template('hello.html', name='hard coded name')
