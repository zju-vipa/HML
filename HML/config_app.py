import os

# Token
SECRET_KEY = 'vipa-hml'

# Database config
# db_host = '10.214.211.205'
db_host = '192.168.1.9'
db_port = 8023
db_name = 'hml'
db_username = 'hml'
db_password = 'hml'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=UTF8MB4&autocommit=true'.format(
    db_username, db_password, db_host, db_port, db_name)

SQLALCHEMY_COMMIT_TEARDOWN = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# test privilege
ROOT_PATH = '/root/HML'
ROOT_FILE_PATH = '/root/HML/Data'
ROOT_MODEL_PATH = '/root/HML/Decision'

SAVE_DATASET_PATH = os.path.join(ROOT_FILE_PATH, 'dataset')
SAVE_TMP_DATASET_PATH = os.path.join(ROOT_FILE_PATH, 'tmp_dataset')
SAVE_PROFILE_PATH = os.path.join(ROOT_FILE_PATH, 'profile')
SAVE_FE_MODEL_PATH = os.path.join(ROOT_MODEL_PATH, 'featureEng')
SAVE_L_MODEL_PATH = os.path.join(ROOT_MODEL_PATH, 'learner')
SAVE_D_RESULT_PATH = os.path.join(ROOT_MODEL_PATH, 'result')
SAVE_PN_DATASET_PATH = os.path.join(ROOT_FILE_PATH, 'power_net_dataset')


if not os.path.exists(SAVE_DATASET_PATH):
    os.mkdir(SAVE_DATASET_PATH)

if not os.path.exists(SAVE_TMP_DATASET_PATH):
    os.mkdir(SAVE_TMP_DATASET_PATH)

if not os.path.exists(SAVE_PROFILE_PATH):
    os.mkdir(SAVE_PROFILE_PATH)

if not os.path.exists(SAVE_FE_MODEL_PATH):
    os.mkdir(SAVE_FE_MODEL_PATH)

if not os.path.exists(SAVE_L_MODEL_PATH):
    os.mkdir(SAVE_L_MODEL_PATH)

if not os.path.exists(SAVE_D_RESULT_PATH):
    os.mkdir(SAVE_D_RESULT_PATH)

if not os.path.exists(SAVE_PN_DATASET_PATH):
    os.mkdir(SAVE_PN_DATASET_PATH)
