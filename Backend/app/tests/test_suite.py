from app.tests.conftest import testClient, dbSession, overrideDbDepend
from app.models.database_models import User, Application
from app.utils.utils import create_user_and_login
from app.utils.utils import get_current_time
import io

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
        

    # Access the user data
    user_data = res_json['user']
    
    username = user_data['username']
    id = user_data['id']


    # Get the user id from the database
    from app.models.database_models import User  # Adjust the import according to your project structure
    user_in_db = dbSession.query(User).filter_by(username='test_user').first()
    assert user_in_db is not None, "User not found in the database"

    # Compare the username and id
    assert user_data['username'] == user_in_db.username
    assert user_data['id'] == user_in_db.id

def test_resume_upload(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

    # Simulating a file upload with a PDF
    file_content = io.BytesIO(b"Test PDF content")  # Simulate the content of the PDF file
    files = {
        'pdf': ('test_resume.pdf', file_content, 'application/pdf')
    }

    # Data to send with the request
    data = {
        'title': 'Test Resume',
        'description': 'This is a test resume'
    }

    # Make the POST request to upload a resume
    res = testClient.post('/resume/upload_resume', data=data, files=files, headers=headers)

    # Check that the request was successful
    assert res.status_code == 201
    assert res.json()['message'] == "Resume uploaded successfully"
    assert 'resume_id' in res.json()

# Test for getting resumes
def test_get_resumes(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

    # Simulate the file upload with multipart/form-data
    file_content = io.BytesIO(b"Test PDF content")  # Simulate the content of the PDF file
    files = {
        'pdf': ('test_resume.pdf', file_content, 'application/pdf')
    }

    # Data to send with the request
    data = {
        'title': 'Test Resume',
        'description': 'This is a test resume'
    }

    # Make the POST request to upload a resume
    upload_resume_response = testClient.post('/resume/upload_resume', data=data, files=files, headers=headers)

    assert upload_resume_response.status_code == 201

    # Make the GET request to get the resumes
    get_resumes_response = testClient.get('/resume/get_resumes', headers=headers)

    assert get_resumes_response.status_code == 200

    # Ensure the uploaded resume is in the response
    resumes = get_resumes_response.json()
    assert any(resume['title'] == 'Test Resume' for resume in resumes)

def test_get_resume_by_title(testClient, dbSession, overrideDbDepend):
    
    headers = create_user_and_login(dbSession, testClient)

    # Simulate the file upload with multipart/form-data
    file_content = io.BytesIO(b"Test PDF content")  # Simulate the content of the PDF file
    files = {
        'pdf': ('test_resume.pdf', file_content, 'application/pdf')
    }

    # Data to send with the request
    data = {
        'title': 'Test Resume',
        'description': 'This is a test resume'
    }

    # Make the POST request to upload a resume
    upload_resume_response = testClient.post('/resume/upload_resume', data=data, files=files, headers=headers)

    assert upload_resume_response.status_code == 201

    # Make the GET request to get the resume by title

    get_resume_response = testClient.get('/resume/get_resume_by_title', params={'title': 'Test Resume'}, headers=headers)

    assert get_resume_response.status_code == 200

    resume_data = get_resume_response.json()
    
    # Verify the title
    assert resume_data['title'] == 'Test Resume'

def test_get_resume_data(testClient, dbSession, overrideDbDepend):
    # Create a user and login
    headers = create_user_and_login(dbSession, testClient)

    # Simulate uploading a PDF resume
    file_content = io.BytesIO(b"Test PDF content")
    files = {
        'pdf': ('test_resume.pdf', file_content, 'application/pdf')
    }
    data = {
        'title': 'Test Resume',
        'description': 'This is a test resume'
    }

    # Upload the resume
    upload_response = testClient.post('/resume/upload_resume', data=data, files=files, headers=headers)
    assert upload_response.status_code == 201
    assert 'resume_id' in upload_response.json()

    # Now, get the PDF data using the title
    get_pdf_response = testClient.get('/resume/get_resume_data', params={'title': 'Test Resume'}, headers=headers)

    # Check the response status code and content type
    assert get_pdf_response.status_code == 200
    assert get_pdf_response.headers['content-type'] == 'application/pdf'

    # Verify the content of the PDF
    assert get_pdf_response.content == b"Test PDF content"

def test_update_resume(testClient, dbSession, overrideDbDepend):
    # Create a user and login
    headers = create_user_and_login(dbSession, testClient)

    # Simulate uploading a PDF resume
    file_content = io.BytesIO(b"Test PDF content")
    files = {
        'pdf': ('test_resume.pdf', file_content, 'application/pdf')
    }
    data = {
        'title': 'Test Resume',
        'description': 'This is a test resume'
    }

    # Upload the resume
    upload_response = testClient.post('/resume/upload_resume', data=data, files=files, headers=headers)
    assert upload_response.status_code == 201
    assert 'resume_id' in upload_response.json()
    
    # Now, update the resume
    updated_data = {
        'description': 'This is an updated test resume',
    }
    
    # Update the resume
    update_resume_response = testClient.put(
        '/resume/update_resume', 
        params={'title': 'Test Resume'},  # Query string for title
        data=updated_data,  # Form data
        headers=headers
    )
    
    assert update_resume_response.status_code == 200
    assert update_resume_response.json()['message'] == 'Resume updated successfully'

    # Verify that the resume was updated in the database
    get_resume_response = testClient.get('/resume/get_resume_by_title', params={'title': 'Test Resume'}, headers=headers)
    assert get_resume_response.status_code == 200
    resume_data = get_resume_response.json()
    
    # Ensure the description was updated
    assert resume_data['description'] == 'This is an updated test resume'   
    
    
def test_delete_resume(testClient, dbSession, overrideDbDepend):
    # Create a user and login
    headers = create_user_and_login(dbSession, testClient)

    # Simulate uploading a PDF resume
    file_content = io.BytesIO(b"Test PDF content")
    files = {
        'pdf': ('test_resume.pdf', file_content, 'application/pdf')
    }
    data = {
        'title': 'Test Resume',
        'description': 'This is a test resume'
    }

    # Upload the resume
    upload_response = testClient.post('/resume/upload_resume', data=data, files=files, headers=headers)
    assert upload_response.status_code == 201
    assert 'resume_id' in upload_response.json()
    
    
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

def test_update_applications(testClient, dbSession, overrideDbDepend):
    headers = create_user_and_login(dbSession, testClient)

    # Make the POST request to create an application
    create_application_response = testClient.post('/application/create_application', json={
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
    
    app_id = create_application_response.json()['application_id']
    
    assert create_application_response.status_code == 201

    # Make the PUT request to update the application
    update_application_response = testClient.put('/application/update_application', json={
        "company": "Pub",
        "position": "GRS",
        "location": "Remote",
        "status": "In Progress",
        "last_update": get_current_time(),
        "salary": "100000",
        "job_description": "No job description",
        "notes": "No notes"
    }, params={'id': app_id}, headers=headers)
    
    updated_application = dbSession.query(Application).filter(Application.id == app_id).first()
    
    assert updated_application is not None
    
    print(update_application_response.json())
    
    assert update_application_response.status_code == 200
    
    assert updated_application.status == "In Progress"
    
    assert updated_application.last_update == get_current_time()
