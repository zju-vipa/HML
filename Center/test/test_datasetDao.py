from dao import DatasetDao
from model import Dataset,db

datasetDao = DatasetDao(db)

def test_addDataset():
    dataset = Dataset()
    dataset.id = "111222333"
    dataset.name = "Cigar"
    dataset.created_by = "123123"
    datasetDao.addDataset(dataset)

def test_deleteDataset():
    datasetDao.deleteDataset("111222333")

def test_updateDataset():
    dataset = datasetDao.queryDatasetById("111222333")
    dataset.dataturks_id = "9999"
    datasetDao.updateDataset(dataset)
    dataset = datasetDao.queryDatasetById("111222333")
    assert dataset.dataturks_id == "9999"

def test_getDatasetList():
    datasets = datasetDao.getDatasetListByUserid("a8439e6632b14b11b62a88a849546658")
    print(datasets)