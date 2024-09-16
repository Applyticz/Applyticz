from conftest import testClient, dbSession, overrideDbDepend
from models.database_models import User

def test_create_user(testClient, dbSession, overrideDbDepend):
    res = testClient.post('/auth/register_account', json={
        'username': 'test_user88',
        'email': 'test88@test.com',
        'password': 'test_password'
    })

    assert res.status_code == 201

def test_update_user(testClient, dbSession, overrideDbDepend):
    # Register a test user
    register_response = testClient.post('/auth/register_account', json={
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test_user@example.com'
    })
    assert register_response.status_code == 201

    # Log in to get an access token
    login_response = testClient.post('/auth/login', data={
        'username': 'test_user',
        'password': 'test_password',
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert login_response.status_code == 200
    access_token = login_response.json()['access_token']

    # Include the access token in the headers
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the PUT request to update the user
    res = testClient.put('/auth/update_account', json={
        'username': 'test_user_update88',
    }, headers=headers)
    assert res.status_code == 201

    # Verify that the user's username has been updated in the database
    updated_user = dbSession.query(User).filter(User.username == 'test_user_update88').first()
    assert updated_user is not None
    assert updated_user.username == 'test_user_update88'

def test_delete_user(testClient, dbSession, overrideDbDepend):
    # Register a test user
    register_response = testClient.post('/auth/register_account', json={
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test_user@example.com'
    })
    assert register_response.status_code == 201

    # Log in to get an access token
    login_response = testClient.post('/auth/login', data={
        'username': 'test_user',
        'password': 'test_password',
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert login_response.status_code == 200
    access_token = login_response.json()['access_token']

    # Include the access token in the headers
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the DELETE request to delete the user
    res = testClient.delete('/auth/delete_account', headers=headers)
    assert res.status_code == 200


def test_get_user(testClient, dbSession, overrideDbDepend):
    # Register a test user
    register_response = testClient.post('/auth/register_account', json={
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test_email@test.com'
    })
    assert register_response.status_code == 201

    # Log in to get an access token
    login_response = testClient.post('/auth/login', data={
        'username': 'test_user',
        'password': 'test_password',
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert login_response.status_code == 200

    access_token = login_response.json()['access_token']

    # Include the access token in the headers
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the GET request to get the user
    res = testClient.get('/auth/get_account', headers=headers)
    assert res.status_code == 200
