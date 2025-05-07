from django.test import TestCase
from unittest import mock
from rest_framework.test import APIClient
from rest_framework import status
from .models import Link
from .config import *

class TestLinkModel(TestCase):
    def setUp(self):
        self.link = Link.objects.create(
            long_link="https://www.example.com",
            code = "Ex4mp7e"
        )
    def test_link_create(self):
        self.assertEqual(self.link.long_link, "https://www.example.com",f"Expected 'https://www.example.com'. Recived {self.link.long_link}")
        self.assertTrue(self.link.code, f"short code does not exist")
        self.assertIsNotNone(self.link.lastUsed, f"lastUsed/createdDate does not exist")
    
    def test_link_create_raises_exception(self):
        with self.assertRaises(Exception):
            Link.objects.create(
                long_link = "https://www.example.com",
                code="Ex4mp7e"
            )

class TestAPIGETRequests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.link = Link.objects.create(
        long_link="https://www.example.com",
        code = "Ex4mp7e"
        )
        Link.objects.create(
            long_link="https://www.example2.com",
        code = "Ex4mp73"
        )
    
    def test_api_default_response(self):
        response = self.client.get(f'/api/')
        self.assertIn("http://link.cbpio.pl:8080/api/v1.0/", response.data, "Default connection does not contain expected data")
        
    def test_api_version_links(self):
        response = self.client.get(f'/api/v1.0/')
        self.assertIn("http://link.cbpio.pl:8080/api/v1.0/short",response.data, f"Expected http://link.cbpio.pl:8080/api/v1.0/short to be in response, expected not in response data")
        self.assertIn("http://link.cbpio.pl:8080/api/v1.0/test",response.data, f"Expected http://link.cbpio.pl:8080/api/v1.0/test to be in response, expected not in response data")
    
    def test_api_redirect_by_short_code(self):
        response = self.client.get(f'/api/v1.0/short/Ex4mp7e')
        self.assertRedirects(response, "https://www.example.com", msg="Expected to redirect user to https://www.example.com. Did not redirect properly")

    def test_api_returns_all_records(self):
        response = self.client.get(f'/api/v1.0/all')
        data = list(Link.objects.all().values())
        self.assertEqual(response.data, data,f"API did not return all records correctly")
    
    def test_api_returns_configuration(self):
        response = self.client.get(f'/api/v1.0/config')
        data =  { 
                "number_of_days":number_of_days,
                "code_length":code_length
                }
        self.assertEqual(data, response.data, f"Did not recive expected values from configuration file")

    def test_api_shows_code_from_long_link(self):
        response = self.client.get(f'/api/v1.0/code/Ex4mp7e')
        self.assertIn("https://www.example.com",response.data,f"API did not return expected long link from given code")
    