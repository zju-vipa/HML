from dao import ModelDao
from model import Model, db

class ModelService:

    def __init__(self):
        self.modelDao = ModelDao(db)

    def getAvaliableModelList(self, userid):
        template = ['id','name','type','code_path', 'config', 'public', 'created_time']
        private_models = self.modelDao.getPrivateModelList(userid)
        public_models = self.modelDao.getPulicModelList()
        private_models.extend(public_models)
        return self.transfer_model_list(private_models, template)

    def transfer_model(self, model, template):
        new_model = {}
        for key in template:
            new_model[key] = getattr(model, key, None)
        return new_model

    def transfer_model_list(self, models, template):
        new_models = []
        for model in models:
            new_models.append(self.transfer_model(model, template))
        return new_models