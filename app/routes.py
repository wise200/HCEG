from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Once a snake, always a snake!!"
