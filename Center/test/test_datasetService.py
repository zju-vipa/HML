from app import datasetService
from model import Dataset

def test_getDatasets():
    datasets = datasetService.getDatasetListByUserid("a8439e6632b14b11b62a88a849546658")
    print("------start to print-------")
    print(datasets)
    for dataset in datasets:
        print(dataset)
    print("------finish to print-------")