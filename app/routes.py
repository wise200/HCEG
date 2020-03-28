from app import app
from flask import render_template, redirect

@app.route('/')
@app.route('/index')
def index():
    info = {'homepage': True}
    return render_template('index.html', info=info)

@app.route('/apply')
def apply():
    info = {'title': 'Apply to HCEG',
            'homepage': False,
            'banner_img': 'apply.jpg'}
    return render_template('apply.html', info=info)

@app.route('/consultforacauseresults19')
def charity():
    return redirect('https://harvardcbe.com')

# dead links
@app.route('/about')
@app.route('/clients')
@app.route('/analysts/overview')
@app.route('/analysts/application')
@app.route('/analysts/experience')
@app.route('/analysts/community')
@app.route('/analysts/faq')
@app.route('/connect')
def random():
    return redirect('https://en.wikipedia.org/wiki/Special:Random')
