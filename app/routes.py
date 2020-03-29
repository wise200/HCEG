from app import app, db, photos
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegistrationForm, CommentForm, RemoveForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Client, Analyst, get_all_items

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
@login_required
def submit():
    info = {'title': 'SUBMIT',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg'}
    return render_template('submit/base.html', info=info)

@app.route('/submit/client', methods=['GET', 'POST'])
@login_required
def submit_client():
    form = CommentForm()
    if form.validate_on_submit():
        filename = photos.save(form.img.data)
        client = Client(name=form.name.data, text=form.text.data, img=filename, author=current_user)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('submit'))
    info = {'title': 'SUBMIT: CLIENT',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg',
            'form': form}
    return render_template('submit/comment.html', info=info)

@app.route('/submit/analyst', methods=['GET', 'POST'])
@login_required
def submit_analyst():
    form = CommentForm()
    if form.validate_on_submit():
        filename = photos.save(form.img.data)
        analyst = Analyst(name=form.name.data, text=form.text.data, img=filename, author=current_user)
        db.session.add(analyst)
        db.session.commit()
        return redirect(url_for('submit'))
    info = {'title': 'SUBMIT: ANALYST',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg',
            'form': form}
    return render_template('submit/comment.html', info=info)

@app.route('/remove', methods=['GET', 'POST'])
@login_required
def remove():
    if request.args.get('id'):
        return remove_item(request.args.get('id'))
    info = {'title': 'REMOVE',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg',
            'content': get_all_items()}
    return render_template('remove.html', info=info)
    '''
    db_items = get_all_items()
    form = RemoveForm()
    form.items.choices = [(item.id, str(item)) for item in db_items]
    if form.validate_on_submit():
        print('data:', form.language.data)
        return redirect(url_for('submit'))
    info = {'title': 'REMOVE',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg',
            'form': form}
    return render_template('remove.html', info=info) '''

@app.route('/remove/<id>')
@login_required
def remove_item(id):
    items = [item for item in get_all_items() if item.id == int(id)]
    print('items:', items)
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('remove'))

@app.route('/consultforacauseresults19')
def charity():
    return redirect('https://harvardcbe.com')

@app.errorhandler(404)
def not_found_error(error):
    info = {'title': 'FILE NOT FOUND',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg'}
    return render_template('errors/404.html', info=info), 404

@app.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    info = {'title': 'SERVER ERROR',
            'homepage': False,
            'banner_img': 'eye_of_providence.jpg'}
    return render_template('errors/500.html', info=info), 500

# dead links
@app.route('/about')
@app.route('/analysts/application')
@app.route('/analysts/experience')
@app.route('/analysts/community')
@app.route('/analysts/faq')
@app.route('/connect')
def random():
    return redirect('https://en.wikipedia.org/wiki/Special:Random')
