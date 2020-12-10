import os

redis_host = '127.0.0.1'
redis_port = 6379
broker_name = '0'
backend_name = '1'

# 设置代理人 broker
broker_url = 'redis://{}:{}/{}'.format(redis_host, redis_port, broker_name)

# 设置结果存储
# lsy_warning: 貌似找不到 backend，无法使用 task.get()
result_backend = 'redis://{}:{}/{}'.format(redis_host, redis_port, backend_name)

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