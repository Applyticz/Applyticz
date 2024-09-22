from app.tests.conftest import testClient, dbSession, overrideDbDepend
from app.models.database_models import User
from app.utils.utils import create_user_and_login
from app.utils.utils import get_current_time

def test_create_user(testClient, dbSession, overrideDbDepend):
    res = testClient.post('/auth/register_account', json={
        'username': 'test_user88',
        'email': 'test88@test.com',
        'password': 'test_password'
    })

    assert res.status_code == 201

def test_update_user(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

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
    headers = create_user_and_login(dbSession, testClient)

    # Make the DELETE request to delete the user
    res = testClient.delete('/auth/delete_account', headers=headers)
    assert res.status_code == 200

def test_get_user(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

    # Make the GET request to get the user
    res = testClient.get('/auth/get_account', headers=headers)
    assert res.status_code == 200

def test_user_data(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

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
    headers = create_user_and_login(dbSession, testClient)

    # Make the POST request to upload a resume

    res = testClient.post('/resume/upload_resume', json={
        'title': 'Test Resume',
        'description': 'This is a test resume',
        'date': '2022-01-01',
        'pdf_url': 'https://example.com/test_resume.pdf'
    }, headers=headers)
    assert res.status_code == 201

def test_get_resumes(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

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

def test_get_resume_by_title(testClient, dbSession, overrideDbDepend):
    
    headers = create_user_and_login(dbSession, testClient)

    # Upload a resume

    upload_resume_response = testClient.post('/resume/upload_resume', json={
        'title': 'Test Resume',
        'description': 'This is a test resume',
        'date': get_current_time(),
        'modified_date': '',
        'pdf_url': 'https://example.com/test_resume.pdf'
    }, headers=headers)

    assert upload_resume_response.status_code == 201

    # Make the GET request to get the resume by title

    get_resume_response = testClient.get('/resume/get_resume_by_title', params={'title': 'Test Resume'}, headers=headers)

    assert get_resume_response.status_code == 200

    resume_data = get_resume_response.json()

    # Verify the title of the resume

    assert resume_data['title'] == 'Test Resume'

    # Verify the description of the resume

    assert resume_data['description'] == 'This is a test resume'

    # Verify the date of the resume

    assert resume_data['date'] == get_current_time()

    # Verify the modified date of the resume

    assert resume_data['modified_date'] == ''

    # Verify the PDF URL of the resume

    assert resume_data['pdf_url'] == 'https://example.com/test_resume.pdf'

def test_update_resume(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

    # Upload a resume
    upload_resume_response = testClient.post('/resume/upload_resume', json={
        'title': 'Test Resume',
        'description': 'This is a test resume',
        'date': '2022-01-01',
        'modified_date': '',
        'pdf_url': 'https://example.com/test_resume.pdf'
    }, headers=headers)
    
    assert upload_resume_response.status_code == 201
    
    # Update the resume
    update_resume_response = testClient.put('/resume/update_resume', json={
        'description': 'This is an updated test resume',
        'pdf_url': 'https://example.com/updated_test_resume.pdf'
    }, params={'title': 'Test Resume'}, headers=headers)
    
    assert update_resume_response.status_code == 201

    # Verify the updated resume
    get_resume_response = testClient.get('/resume/get_resume_by_title', params={'title': 'Test Resume'}, headers=headers)
    assert get_resume_response.status_code == 200

    resume_data = get_resume_response.json()

    # Verify the updated description
    assert resume_data['description'] == 'This is an updated test resume'

    # Verify the updated PDF URL
    assert resume_data['pdf_url'] == 'https://example.com/updated_test_resume.pdf'

    # Verify the modified date is updated
    assert resume_data['modified_date'] != ''  # Ensure modified_date is not empty
    
def test_delete_resume(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

    # Upload a resume
    upload_resume_response = testClient.post('/resume/upload_resume', json={
        'title': 'Test Resume',
        'description': 'This is a test resume',
        'date': '2022-01-01',
        'pdf_url': 'https://example.com/test_resume.pdf'
    }, headers=headers)

    assert upload_resume_response.status_code == 201

    # Make the DELETE request to delete the resume
    delete_resume_response = testClient.delete('/resume/delete_resume', params={'title': 'Test Resume'}, headers=headers)

    assert delete_resume_response.status_code == 200

def test_create_application(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

    # Make the POST request to create an application
    create_application_response = testClient.post('/application/create_application', json={
        "id": "App",
        "company": "Pub",
        "position": "GRS",
        "location": "Remote",
        "status": "New",
        "applied_date": "09-09-2024",
        "last_update": "",
        "salary": "100000",
        "job_description": "No job description",
        "notes": "No notes"
    }, headers=headers)

    assert create_application_response.status_code == 201

def test_get_applications(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

    # Make the POST request to create an application
    create_application_response = testClient.post('/application/create_application', json={
        "id": "App",
        "company": "Pub",
        "position": "GRS",
        "status": "New",
        "applied_date": "09-09-2024",
        "notes": "No notes"
    }, headers=headers)

    # Make the GET request to get the applications
    get_applications_response = testClient.get('/application/get_applications', headers=headers)
    
    assert get_applications_response.status_code == 200
