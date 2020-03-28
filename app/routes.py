from app import app, db
from flask import render_template, redirect, url_for
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

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
    if current_user.is_authenticated:
        return redirect(url_for('submit'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Invalid username', 'error')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Invalid password', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('submit'))
    info = {'title': 'DIVINE VERIFICATION',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg',
            'form': form}
    return render_template('login.html', info=info)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('submit'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    info = {'title': 'DIVINE VERIFICATION',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg',
            'form': form}
    return render_template('register.html', info=info)

@app.route('/submit')
def submit():
    return redirect(url_for('index'))

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
