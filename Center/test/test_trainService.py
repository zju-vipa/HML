from app import trainService
from model import Train


def test_acceptTrain():
    trainService.acceptTrain('82de87a2d482460b98123aebf842da51',
                             '65c8d0a5339642fb8689ede14ddbbffd')