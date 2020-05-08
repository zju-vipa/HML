from flask import Flask, render_template
from app.db import db

"""
app init
"""

app = Flask(__name__)

# connect the sql
app.config.from_object('config_app')
db.init_app(app)
app.app_context().push()

# root page
@app.route('/')
def index():
    return render_template('index.html')

# hello
@app.route('/hello', methods=['GET', 'POST'])
def hello_world():
    return 'hello world'


# register blueprint
from app import _UserApp, _DatasetApp, _FeatureEngApp, _LearnerApp, _DecisionApp, _AlgorithmApp
app.register_blueprint(_UserApp.bp)
app.register_blueprint(_DatasetApp.bp)
app.register_blueprint(_FeatureEngApp.bp)
app.register_blueprint(_LearnerApp.bp)
app.register_blueprint(_DecisionApp.bp)
app.register_blueprint(_AlgorithmApp.bp)

# db init
db.create_all()
db.session.commit()
