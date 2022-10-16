import pytest
import random


@pytest.fixture(scope='module')
def test_user():
    return f'user_{random.randint(100,200)}'


def test_fixture_1(test_user):
    assert test_user == 101

def test_fixture_2(test_user):
    assert test_user == 250