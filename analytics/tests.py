from rest_framework.test import APITestCase
from analytics.models import Event
from django.urls import reverse
from rest_framework import status


class EventTests(APITestCase):
    def url(self):
        return reverse('events')
    
    #positive test cases
    def test_basic_event_create(self):
        data = {'name': 'foo'}
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(),1)
        self.assertEqual(Event.objects.get().name, 'foo') 
    
    def test_extended_event_create(self):
        data = {'name': 'foo', 'additional_data': 'bar'}
        response = self.client.post(self.url(), data, format='json')
        obj = Event.objects.get()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(obj.name, 'foo')
        self.assertEqual(obj.additional_data, 'bar')

    #negative test cases
    def test_wrong_request_type(self):
        data = {'name': 'foo', 'additional_data':'bar'}
        response = self.client.get(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_no_parameters(self):
        data = dict()
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 0)
    
    def test_empty_name_parameter(self):
        data = {'name': ''}
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 0)

    def test_too_long_name_parameter(self):
        data = dict()
        with open('./analytics/testing_resources/testing_template_text.txt', 'r') as f:
            data['name'] = f.read()
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(),0)
    
    def test_wrong_request_parameters(self):
        data = {'nam' : 'foo'}
        response = self.client.post(self.url(), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 0)
