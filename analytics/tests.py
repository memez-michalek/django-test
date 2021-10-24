from rest_framework.test import APITestCase
from analytics.models import Event
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class EventTests(APITestCase):
    def url(self):
        return reverse('events')
    def create_user_token(self):
        user = User.objects.create(username='admin', password='admin')
        user.save()
        return Token.objects.get(user=user).key
    
    #positive test cases

    def test_basic_event_create(self):
        token = self.create_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'foo'}
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(),1)
        self.assertEqual(Event.objects.get().name, 'foo') 
    
    def test_extended_event_create(self):
        token = self.create_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'foo', 'additional_data': 'bar'}
        response = self.client.post(self.url(), data, format='json')
        obj = Event.objects.get()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(obj.name, 'foo')
        self.assertEqual(obj.additional_data, 'bar')

    #negative test cases
    def test_wrong_request_type(self):
        token = self.create_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'foo', 'additional_data':'bar'}
        response = self.client.get(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_no_parameters(self):
        token = self.create_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = dict()
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 0)

    
    def test_empty_name_parameter(self):
        token = self.create_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': ''}
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 0)

    def test_too_long_name_parameter(self):
        token = self.create_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = dict()
        with open('./analytics/testing_resources/testing_template_text.txt', 'r') as f:
            data['name'] = f.read()
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(),0)
    
    def test_wrong_request_parameters(self):
        token = self.create_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'nam' : 'foo'}
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 0)
    
    def test_no_authorization_header(self):
        data = {'name' : 'foo'}
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Event.objects.count(),0)
    
    def test_invalid_authorization_header(self):
        token = '123456789'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name' : 'foo'}
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_instead_of_bearer(self):
        token = self.create_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = {'name' : 'foo'}
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

