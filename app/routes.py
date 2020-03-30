from app import app, db, photos
from flask import render_template, redirect, url_for, flash, request, abort
from app.forms import LoginForm, RegistrationForm, CommentForm, PageForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *

DEFAULT_IMAGE = 'eye_of_providence.jpg'
DEFAULT_CLIENT = Client(name='HCEG', text='We have no clients right now. We are sad.')
possible_paths = set(['/about',
                      '/analysts/application',
                      '/analysts/experience',
                      '/analysts/community',
                      '/analysts/faq',
                      '/connect'])

@app.route('/')
@app.route('/index')
def index():
    images = [client.img for client in Client.query.all()]
    images = images[:16]
    info = {'homepage': True,
            'images': images}
    return render_template('index.html', info=info)

@app.route('/apply')
def apply():
    info = {'title': 'Apply to HCEG',
            'homepage': False,
            'banner_img': 'money.jpg'}
    return render_template('apply.html', info=info)

@app.route('/clients')
def clients():
    clients_list = Client.query.all()
    first, second = get_columns(clients_list)
    images = [client.img for client in clients_list]
    images = images[:16]
    info = {'title': 'CLIENTS',
            'homepage': False,
            'banner_img': DEFAULT_IMAGE,
            'firstcolumn': first,
            'secondcolumn': second,
            'images': images}
    return render_template('clients.html', info=info)

@app.route('/analysts/overview')
def analysts_overview():
    analysts = Analyst.query.all()
    info = {'title': 'OVERVIEW',
            'homepage': False,
            'banner_img': 'money.jpg',
            'content': analysts}
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
            'banner_img': DEFAULT_IMAGE,
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
            'banner_img': DEFAULT_IMAGE,
            'form': form}
    return render_template('register.html', info=info)

@app.route('/submit')
@login_required
def submit():
    info = {'title': 'SUBMIT',
            'homepage': False,
            'banner_img': DEFAULT_IMAGE}
    return render_template('submit/base.html', info=info)

@app.route('/submit/client', methods=['GET', 'POST'])
@login_required
def submit_client():
    form = CommentForm()
    if form.validate_on_submit():
        filename = photos.save(form.img.data)
        file_url = photos.url(filename)
        client = Client(name=form.name.data, text=form.text.data, img=file_url, author=current_user)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('submit'))
    info = {'title': 'SUBMIT: CLIENT',
            'homepage': False,
            'banner_img': DEFAULT_IMAGE,
            'form': form}
    return render_template('submit/comment.html', info=info)

@app.route('/submit/analyst', methods=['GET', 'POST'])
@login_required
def submit_analyst():
    form = CommentForm()
    if form.validate_on_submit():
        filename = photos.save(form.img.data)
        file_url = photos.url(filename)
        analyst = Analyst(name=form.name.data, text=form.text.data, img=file_url, author=current_user)
        db.session.add(analyst)
        db.session.commit()
        return redirect(url_for('submit'))
    info = {'title': 'SUBMIT: ANALYST',
            'homepage': False,
            'banner_img': DEFAULT_IMAGE,
            'form': form}
    return render_template('submit/comment.html', info=info)

@app.route('/submit/page')
@login_required
def choose_page():
    if request.args.get('chosen_path'):
        return submit_page(request.args.get('chosen_path'))
    pages = Page.query.all()
    used_paths = set([page.path for page in pages])
    paths = list(possible_paths - used_paths)
    paths = [encode_path(path) for path in sorted(paths)]
    info = {'title': 'CHOOSE PAGE',
            'homepage': False,
            'banner_img': DEFAULT_IMAGE,
            'paths': paths}
    return render_template('submit/choose_page.html', info=info)

@app.route('/submit/page/<path>', methods=['GET', 'POST'])
@login_required
def submit_page(path):
    path = decode_path(path)
    form = PageForm()
    if form.validate_on_submit():
        photo = form.img.data
        filename = photos.save(photo) if photo else DEFAULT_IMAGE
        page = Page(path=path, title=form.title.data, text=form.text.data, img=filename, author=current_user)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('submit'))
    info = {'title': 'SUBMIT: PAGE',
            'homepage': False,
            'banner_img': DEFAULT_IMAGE,
            'form': form,
            'path': path}
    return render_template('submit/page.html', info=info)

@app.route('/remove')
@login_required
def remove():
    arg_id = request.args.get('id')
    arg_confirm = request.args.get('confirm')
    arg_class = request.args.get('classname')
    if arg_id:
        if arg_confirm:
            return redirect(url_for('remove_item', classname=arg_class, id=arg_id))
        item = get_item(int(arg_id), arg_class)
        if item == -1:
            return abort(404)
        # make item easily parseable for html
        item = item.__dict__
        if item['_sa_instance_state']:
            item.pop('_sa_instance_state')
        info = {'title': 'CONFIRMATION',
                'homepage': False,
                'banner_img': DEFAULT_IMAGE,
                'content': item}
        return render_template('remove_confirm.html', info=info)
    info = {'title': 'REMOVE',
            'homepage': False,
            'banner_img': DEFAULT_IMAGE,
            'content': get_all_items()}
    return render_template('remove.html', info=info)

@app.route('/remove/<classname>/<id>')
@login_required
def remove_item(classname, id):
    item = get_item(int(id), classname)
    if item == -1:
        return abort(404)
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
            'banner_img': DEFAULT_IMAGE}
    return render_template('errors/404.html', info=info), 404

@app.errorhandler(500)
def server_error(error):
    db.session.rollback()
    info = {'title': 'SERVER ERROR',
            'homepage': False,
            'banner_img': DEFAULT_IMAGE}
    return render_template('errors/500.html', info=info), 500

# dead links
@app.route('/about')
@app.route('/analysts/application')
@app.route('/analysts/experience')
@app.route('/analysts/community')
@app.route('/analysts/faq')
@app.route('/connect')
def custom_pages():
    page = Page.query.filter_by(path=request.path).first()
    if page:
        info = {'title': page.title,
                'homepage': False,
                'banner_img': DEFAULT_IMAGE,
                'text': page.text}
        return render_template('custom.html', info=info)
    # uncoment this to redirect unfilled links to a random wikipedia page instead of throwing a 404
    # return redirect('https://en.wikipedia.org/wiki/Special:Random')
    return abort(404)

def encode_path(path):
    return path.replace('/', ':')

def decode_path(path):
    return path.replace(':', '/')

# split the clients list into two columns
def get_columns(clients):
    if len(clients) == 0:
        return [DEFAULT_CLIENT], []
    partition = len(clients) // 2
    first = clients[:partition]
    second = clients[partition:]
    return first, second
