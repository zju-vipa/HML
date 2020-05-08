import os

# LOCAL_DATABASE = os.path.join('app/instance', 'app.sqlite')
SECRET_KEY = 'vipa-aix'

# database
# center
center_db_host = '10.214.211.205'
center_db_port = 8022223
center_db = 'hm22l'
center_db_username, center_db_password = 'hml', 'hml'

# must +pymysql
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    center_db_username, center_db_password, center_db_host, center_db_port,
    center_db)

# # dataturks
# dataturks_db_host = '10.214.211.205'
# DATATURKS_INDEX = 'http://' + dataturks_db_host
# DATATURKS_BASE = DATATURKS_INDEX + '/dataturks'


SQLALCHEMY_COMMIT_TEARDOWN = False  # auto commit db changes
SQLALCHEMY_TRACK_MODIFICATIONS = False
