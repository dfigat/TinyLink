from django.test import TestCase
from unittest import mock
from rest_framework.test import APIClient
from rest_framework import status
from .models import Link
from .config import *
import datetime

class TestLinkModel(TestCase):
    def setUp(self):
        self.link = Link.objects.create(
            long_link="https://www.example.com",
            code = "Ex4m"
        )
    def test_link_create(self):
        self.assertEqual(self.link.long_link, "https://www.example.com",f"Expected 'https://www.example.com'. Recived {self.link.long_link}")
        self.assertTrue(self.link.code, f"short code does not exist")
        self.assertIsNotNone(self.link.lastUsed, f"lastUsed/createdDate does not exist")
    
    def test_link_create_raises_exception(self):
        with self.assertRaises(Exception):
            Link.objects.create(
                long_link = "https://www.example.com",
                code="Ex4m"
            )

class TestAPIGETRequests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.link = Link.objects.create(
        long_link="https://www.example.com",
        code = "Ex4m",
        lastUsed = datetime.datetime(2025,4,9,7,13,32,358992,tzinfo=datetime.timezone.utc)
        )
        Link.objects.create(
            long_link="https://www.example2.com",
            code = "Ex4w"
        )
    
    def test_api_default_response(self):
        response = self.client.get(f'/api/')
        self.assertIn("http://link.cbpio.pl:8080/api/v1.0/", response.data, "Default connection does not contain expected data")
        
    def test_api_version_links(self):
        response = self.client.get(f'/api/v1.0/')
        self.assertIn("http://link.cbpio.pl:8080/api/v1.0/short",response.data, f"Expected http://link.cbpio.pl:8080/api/v1.0/short to be in response, expected not in response data")
        self.assertIn("http://link.cbpio.pl:8080/api/v1.0/test",response.data, f"Expected http://link.cbpio.pl:8080/api/v1.0/test to be in response, expected not in response data")
    
    def test_api_redirect_by_short_code(self):
        response = self.client.get(f'/api/v1.0/short/Ex4m', follow=False)
        self.assertEqual(response.status_code, 301)# 301 is code for redirect
        
    def test_api_returns_all_records(self):
        response = self.client.get(f'/api/v1.0/all')
        data = list(Link.objects.all().values())
        expectedPairs = [(item['long_link'], item['code'])for item in data]
        recivedPairs =  [(item['long_link'], item['code'])for item in response.json()]
        self.assertEqual(expectedPairs, recivedPairs,f"API did not return all records correctly")

    def test_api_returns_configuration(self):
        response = self.client.get(f'/api/v1.0/config')
        data =  { 
                "number_of_days":number_of_days,
                "code_length":code_length
                }
        self.assertEqual(data, response.data, f"Did not recive expected values from configuration file")

    # def test_api_shows_code_from_long_link(self):
    #     response = self.client.get(f'/api/v1.0/code/https://www.example.com')
    #     self.assertIn("Ex4m",response,f"API did not return expected long link from given code")
    
class TestAPIDELETERequests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.link = Link.objects.create(
        long_link="https://www.example.com",
        code = "Ex4m",
        lastUsed = datetime.datetime(2025,4,9,7,13,32,358992,tzinfo=datetime.timezone.utc)
        )
        Link.objects.create(
            long_link="https://www.example2.com",
            code = "Ex4w"
        )
        
    def test_api_delete_all_by_treshold(self):
        preDelete = Link.objects.all()
        response = self.client.delete(f"/api/v1.0/short/delete_old")
        postDelete = Link.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(preDelete,postDelete)

class TestAPIPOSTRequest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Link.objects.create(
           long_link="https://www.example.com",
            code = "Ex4m" 
        )
