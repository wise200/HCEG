from app import app
from flask import render_template, redirect, url_for
from app.forms import LoginForm

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

@app.route('/clients')
def clients():
    info = {'title': 'CLIENTS',
            'homepage': False,
            'banner_img': 'clients.jpg'}
    return render_template('clients.html', info=info)

@app.route('/analysts/overview')
def analysts_overview():
    info = {'title': 'OVERVIEW',
            'homepage': False,
            'banner_img': 'apply.jpg'}
    return render_template('analysts_overview.html', info=info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Login requested for user {} with pass {}'.format(form.username.data, form.password.data))
        return redirect(url_for('index'))
    info = {'title': 'DIVINE VERIFICATION',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg',
            'form': form}
    return render_template('login.html', info=info)

@app.route('/consultforacauseresults19')
def charity():
    return redirect('https://harvardcbe.com')

# dead links
@app.route('/about')
@app.route('/analysts/application')
@app.route('/analysts/experience')
@app.route('/analysts/community')
@app.route('/analysts/faq')
@app.route('/connect')
def random():
    return redirect('https://en.wikipedia.org/wiki/Special:Random')
