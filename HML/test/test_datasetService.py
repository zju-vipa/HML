from app._DatasetApp import datasetService
from model import Dataset


def test_addDataset():
    dataset_bean = Dataset()
    dataset_bean.dataset_id = "477af5c390569f7994c8cd9f93a182a4"
    dataset_bean.dataset_name = "qwqwqw"
    dataset_bean.file_type = "csv"
    dataset_bean.user_id = "123123"
    dataset_bean.username = "2131"
    dataset = datasetService.addDataset(dataset_bean).serialize
    print("------start to print-------")
    print(dataset)
    print("------finish to print-------")


def test_getDatasetById():
    dataset = datasetService.getDatasetById("a0bcd131560444698fc1b5531c2c5608")
    if dataset:
        dataset = dataset.serialize
    print("------start to print-------")
    print(dataset)
    print("------finish to print-------")


def test_getDatasetListByUserId():
    datasets = datasetService.getDatasetListByUserId("b05a36ac41de45b1880f7facd5bd4169")
    if datasets:
        datasets = [dataset.serialize for dataset in datasets]
    print("------start to print-------")
    if datasets:
        for dataset in datasets:
            print(dataset)
    print("------finish to print-------")


def test_updateDataset():
    dataset_bean = datasetService.getDatasetById("809a8af951c24d4fb4bcb0ed3db8e86a")
    dataset_bean.user_id = "1231231231231"
    result = datasetService.updateDataset(dataset_bean)
    print("------start to print-------")
    print(result)
    print("------finish to print-------")


def test_deleteDataset():
    result = datasetService.deleteDataset("a0bcd131560444698fc1b5531c2c5608")
    print("------start to print-------")
    print(result)
    print("------finish to print-------")


def test_deleteDataset():
    result = datasetService.deleteDataset("a0bcd131560444698fc1b5531c2c5608")
    print("------start to print-------")
    print(result)
    print("------finish to print-------")






