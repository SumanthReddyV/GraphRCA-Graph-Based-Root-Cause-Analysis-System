from auth import login

def test_login():
    assert login() == 200