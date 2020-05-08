from app import modelService

def test_modelList():
    models = modelService.getAvaliableModelList('a8439e6632b14b11b62a88a849546658')
    print(models)
    print(len(models))