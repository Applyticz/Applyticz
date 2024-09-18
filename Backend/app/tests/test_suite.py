from app.tests.conftest import testClient, dbSession, overrideDbDepend
from app.models.database_models import User

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
        'email': 'test@test.com',
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

def test_user_data(testClient, dbSession, overrideDbDepend):
    # Register a test user
    register_response = testClient.post('/auth/register_account', json={
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test@test.com'
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

    # Make the GET request to get the user data
    res = testClient.get('/auth/', headers=headers)
    assert res.status_code == 200

    res_json = res.json()

    # Verify that 'User' key exists
    assert 'User' in res_json, "Response JSON does not contain 'User' key"

    # Access the user data
    user_data = res_json['User']

    # Compare the username
    assert user_data['username'] == 'test_user'

    # Get the user id from the database
    from app.models.database_models import User  # Adjust the import according to your project structure
    user_in_db = dbSession.query(User).filter_by(username='test_user').first()
    assert user_in_db is not None, "User not found in the database"

    # Compare the user id
    assert user_data['id'] == user_in_db.id

def test_resume_upload(testClient, dbSession, overrideDbDepend):
    # Register a test user
    register_response = testClient.post('/auth/register_account', json={
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test@test.com',
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

    # Make the POST request to upload a resume

    res = testClient.post('/resume/upload_resume', json={
        'title': 'Test Resume',
        'description': 'This is a test resume',
        'date': '2022-01-01',
        'pdf_url': 'https://example.com/test_resume.pdf'
    }, headers=headers)
    assert res.status_code == 201

def test_get_resumes(testClient, dbSession, overrideDbDepend):
    # Register a test user
    register_response = testClient.post('/auth/register_account', json={
        'username': 'test_user',
        'password': 'test_password',
        'email': 'test@test.com',
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

    # Make the POST request to upload a resume

    upload_resume_response = testClient.post('/resume/upload_resume', json={
        'title': 'Test Resume',
        'description': 'This is a test resume',
        'date': '2022-01-01',
        'pdf_url': 'https://example.com/test_resume.pdf'
    }, headers=headers)

    assert upload_resume_response.status_code == 201

    # Make the GET request to get the resumes

    get_resumes_response = testClient.get('/resume/get_resumes', headers=headers)

    assert get_resumes_response.status_code == 200



