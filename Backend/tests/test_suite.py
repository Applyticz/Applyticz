from conftest import testClient, dbSession, overrideDbDepend

def test_create_test(testClient, dbSession, overrideDbDepend):
    res = testClient.post('/test/create_test', json={
        'username': 'test_user',
        'email': 'test@test.com',
        'password': 'test_password'
    })

    assert res.status_code == 201

def test_get_all_tests(testClient, dbSession, overrideDbDepend):
    res = testClient.get('/test/get_all_tests')

    assert res.status_code == 200