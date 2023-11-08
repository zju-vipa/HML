from flask import Blueprint, request, json
from app.constant import get_error, RET
from app._UserApp import login_required
from model import Algorithm
from service import AlgorithmService
algorithmService = AlgorithmService()

bp = Blueprint('algorithm', __name__, url_prefix='/api/private/v1/algorithm')


@bp.route('/query', methods=('GET', 'POST'))
@login_required
def query_algorithm_list():
    if request.method == 'GET':
        try:
            algorithm_category = request.args.get('algorithm_category')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not algorithm_category:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_category')

        algorithms = algorithmService.queryAlgorithmListByCategory(algorithm_category)
        if algorithms:
            algorithms = [algorithm.serialize for algorithm in algorithms]
        else:
            algorithms = None
        return {'meta': {'msg': 'query algorithm list success', 'code': 200}, 'data': algorithms}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

@bp.route('/queryIntroductions', methods=('GET', 'POST'))
@login_required
def query_train_methods_introductions():
    # 训练方法
    # trainMethod_HML_RL trainMethod_RFC trainMethod_LR trainMethod_SVM
    print('query_train_methods_introductions')
    learnerTrainMethodsNames = ['HML_RL', 'RFC', 'LR', 'SVM']
    if request.method == 'GET':
        try:
            trainName = request.args.get('trainName')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not trainName:
            return get_error(RET.PARAMERR, 'Error: request lacks trainName')
        print('trainName:', trainName)
        img_url = "http://10.82.29.169:8030/img/trainMethod_" + trainName + ".jpg"
        trainMethodsIntro={}
        trainMethodsIntro['image_url']=img_url
        if trainName==learnerTrainMethodsNames[0]:
          trainMethodsIntro['name']='基于强化学习的主动性人在回路双向学习方法'
          trainMethodsIntro['describe']='在学习过程中利用主动问询机制获取专家对困难样本的解决方案，智能体通过模仿学习训练这些典型样本，并将任务泛化到其他相似样本，在大幅度降低交互需求的同时，仍能保证与持续监督方法有相当的性能，极大提高训练过程中的采样效率。'
        elif trainName==learnerTrainMethodsNames[1]:
          trainMethodsIntro['name']='随机森林方法（RFC）'
          trainMethodsIntro['describe']='一种基于多个决策树的集成学习算法，通过从原始数据集中随机抽样构建多个决策树并集成它们的预测结果，来提高模型的准确性和稳定性。'
        elif trainName==learnerTrainMethodsNames[2]:
          trainMethodsIntro['name']='逻辑回归方法（LR）'
          trainMethodsIntro['describe']='一种二分类方法，通过将特征的加权和通过一个逻辑函数转换，该函数能够将任何实数值映射到0和1之间，从而得到一个处于这个区间内的概率值。逻辑回归模型训练时，会寻找最佳的权重，以最小化预测概率与实际发生结果之间的差异。'
        elif trainName==learnerTrainMethodsNames[3]:
          trainMethodsIntro['name']='支持向量机方法（SVM）'
          trainMethodsIntro['describe']='核心思想是找到能够最大化不同类别数据点间隔的分界线或超平面。在处理线性不可分数据时，SVM通过引入核技巧，将数据映射到更高维空间，以寻找合适的分隔超平面。这种方法对于小样本和高维数据表现出色，且具有良好的泛化能力。'
        print('trainMethodsIntro3:', trainMethodsIntro)
          
        return {'meta': {'msg': 'query algorithm list success', 'code': 200}, 'data': trainMethodsIntro}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_algorithm():
    """
    add a algorithm using the params in request
    :return:
    """
    if request.method == 'POST':
        try:

            algorithm_name = request.json.get('algorithm_name')
            algorithm_type = request.json.get('algorithm_type')
            algorithm_category = request.json.get('algorithm_category')
            algorithm_parameters = request.json.get('algorithm_parameters')
            introduction = request.json.get('introduction')
        except Exception:
            return get_error(RET.PARAMERR, 'Error: no request')

        if not algorithm_name:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_name')
        if not algorithm_type:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_type')
        if not algorithm_category:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_category')
        if not algorithm_parameters:
            return get_error(RET.PARAMERR, 'Error: request lacks algorithm_parameters')

        algorithm_bean = Algorithm()
        algorithm_bean.algorithm_name = algorithm_name
        algorithm_bean.algorithm_type = algorithm_type
        algorithm_bean.algorithm_category = algorithm_category
        algorithm_bean.algorithm_parameters = json.dumps(algorithm_parameters, ensure_ascii=False)
        algorithm_bean.introduction = introduction

        algorithm = algorithmService.addAlgorithm(algorithm_bean).serialize

        return {'meta': {'msg': 'add algorithm success', 'code': 200}, 'data': algorithm}, 200
    return {'meta': {"msg": "method not allowed", 'code': 405}}, 405
