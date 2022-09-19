from pydoc import cli
import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course

@pytest.fixture
def client():
    return APIClient()
# end client()

@pytest.fixture
def course_factory():
    
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    
    return factory
# end course_factory()

@pytest.mark.django_db
def test_first_course(client, course_factory):
    # Arrange
    courses = course_factory(name='1')
    
    #Act
    response1 = client.get('/api/v1/courses/1/')
    
    print(response1)
    
    #Assert
    assert response1.status_code == 200
    data = response1.json()
    assert data.get('name') == '1'
    
# end test_first_course()

@pytest.mark.django_db
def test_list_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=5)
    
    #Act
    response = client.get('/api/v1/courses/')
    
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    
# end test_list_course()

@pytest.mark.django_db
def test_id_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=5)
    
    #Act
    id = courses[0].id
    response = client.get(f'/api/v1/courses/?id={id}')
    
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    
# end test_id_course()

@pytest.mark.django_db
def test_name_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=5)
    
    #Act
    name = courses[0].name
    response = client.get(f'/api/v1/courses/?name={name}')
    
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    
# end test_name_course()

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    
    data = {'name': 'c++', 'students': []}
    response = client.post('/api/v1/courses/', data=data, format='json')
    
    assert response.status_code == 201
    
    count2 = Course.objects.count()
    
    assert count2 > count
# end test_create_course()

@pytest.mark.django_db
def test_update_course(client, course_factory):

    courses = course_factory(_quantity=5)
    
    id = courses[0].id
    response = client.get(f'/api/v1/courses/?id={id}')
    assert response.status_code == 200
    
    data = response.json()
    data[0]['name'] = 'updated'
    #data = {'name': 'updated'}
    
    response = client.post(f'/api/v1/courses/', data=data[0], format='json')
    assert response.status_code == 201
    
    response = client.get(f'/api/v1/courses/?name=updated')
    assert response.status_code == 200
    
    data = response.json()
    assert data[0].get('name') == 'updated'
    
# end test_update_course()

@pytest.mark.django_db
def test_delete_course(client):
    
    course = Course.objects.create(name='delete')
    
    count = Course.objects.count()
    
    response = client.delete(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 204
    
    count2 = Course.objects.count()
    
    assert count > count2
# end test_create_course()