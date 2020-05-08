from celery import Celery
import sys


celery_app = Celery('celery_tasks.tasks')

# 从单独的配置模块中加载配置
celery_app.config_from_object('celery_tasks.config_celery')

# 设置项目根目录
sys.path.append(celery_app.conf["ROOT_PATH"])

# 自动搜索任务
celery_app.autodiscover_tasks(['celery_tasks.tasks'])

