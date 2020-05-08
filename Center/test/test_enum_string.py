from enum import Enum

class TestEnum(Enum):
    A = 1
    B = 2
    C = 3

def test_enum_string():
    x = 'A'
    y = 'X'

    a = TestEnum[x]
    b = TestEnum.__contains__(y)
    print(a)
    print(b)