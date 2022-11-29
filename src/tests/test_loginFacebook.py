import pytest
from app import facebook_auth

def test_suma():
    response = facebook_auth()
    assert response == True
    assert responser == False 