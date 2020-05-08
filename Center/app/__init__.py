from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
sql_db = SQLAlchemy(app)
print("sql_db created...")

from service import (
    UserService, DatasetService, ModelService, TaskService, DeviceService, TrainService,
    DataturksUserService, DataturksProjectService
)
userService: UserService = UserService()
datasetService:DatasetService = DatasetService()
modelService:ModelService = ModelService()
taskService:TaskService = TaskService()
deviceService:DeviceService = DeviceService()
trainService = TrainService()
dataturksUserService = DataturksUserService()
dataturksProjectService = DataturksProjectService()

@app.route('/')
def index():
    # do this when start the web
    return render_template('index.html')


from app import auth, task, dataset, model, device, train
#
app.register_blueprint(auth.bp)
# app.register_blueprint(task.bp)
# app.register_blueprint(dataset.bp)
# app.register_blueprint(model.bp)
# app.register_blueprint(device.bp)
# app.register_blueprint(train.bp)
