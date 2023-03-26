import os

from flask import Flask, render_template
from flask_restful import Api
from flask_bootstrap import Bootstrap4
from dotenv import load_dotenv
from views import views_blueprint

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap4(app)
api = Api(app)
app.register_blueprint(views_blueprint)
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/personal')
def personal():
    return render_template('personal_info.html')


@app.route('/work')
def work():
    return render_template('work.html')


@app.route('/education')
def education():
    return render_template('education.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/additional')
def additional():
    return render_template('additional.html')


@app.route('/finish')
def finish():
    return render_template('finish.html')


if __name__ == "__main__":
    app.run(debug=True)
