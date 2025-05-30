from django.test import TestCase
from unittest import mock
from rest_framework.test import APIClient
from rest_framework import status
from .models import Link
from .config import *
from dotenv import load_dotenv
from django.test import override_settings
import os
import datetime
load_dotenv('../db/.env')
URL = os.getenv('API_URL')
URL_SHORT = os.getenv('API_URL_SHORTENED')

class TestLinkModel(TestCase):
    def setUp(self):
        self.link = Link.objects.create(
            long_link="https://www.example.com",
            code = "Ex4m"
        )
        """ Testuje tworzenie nowego linku w bazie danych"""
    def test_link_create(self):
        self.assertEqual(self.link.long_link, "https://www.example.com",f"Expected 'https://www.example.com'. Recived {self.link.long_link}")
        self.assertTrue(self.link.code, f"short code does not exist")
        self.assertIsNotNone(self.link.lastUsed, f"lastUsed/createdDate does not exist")
    
    """ Testuje czy rzuca błąd gdy próbuje tworzyć link z tymi samymi danymi """
    def test_link_create_raises_exception(self):
        with self.assertRaises(Exception):
            Link.objects.create(
                long_link = "https://www.example.com",
                code="Ex4m"
            )
@override_settings(SECURE_SSL_REDIRECT=False)
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
    """ Testuje czy odpowiedź servera na zapytanie działa"""
    def test_api_default_response(self):
        response = self.client.get(f'/api/', follow=False)
        print('f1',response.data)
        self.assertTrue(response.data[0].startswith(f"{URL}v{API_VERSION}"))

    """ Testuje czy server poprawnie odpowiada na zapytanie"""
    def test_api_version_links(self):
        response = self.client.get(f'/api/v{API_VERSION}', follow=True, headers={'Authorization':'Bearer {self.access_token}'})
        print('f2',response.data)
        self.assertIn(f"{URL}v{API_VERSION}/short",response.content.decode('utf-8'))#, f"Expected http://link.cbpio.pl:8080/api/v{API_VERSION}/short to be in response, expected not in response data")
        self.assertIn(f"{URL}v{API_VERSION}/test",response.content.decode('utf-8'))#, f"Expected http://link.cbpio.pl:8080/api/v{API_VERSION}/test to be in response, expected not in response data")
    
    """ Testuje czy server poprawnie przekierowuje użytkownika po podaniu kodu"""
    def test_api_redirect_by_short_code(self):
        response = self.client.get(f'/api/v{API_VERSION}/short/Ex4m', follow=False)
        self.assertEqual(response.status_code, 301)

    """ Testuje czy server poprawnie zwraca wszystkie linki i ich kody z bazy danych"""    
    def test_api_returns_all_records(self):
        response = self.client.get(f'{URL}v{API_VERSION}/all')
        data = list(Link.objects.all().values())
        expectedPairs = [(item['long_link'], item['code'])for item in data]
        recivedPairs =  [(item['long_link'], item['code'])for item in response.json()]
        self.assertEqual(expectedPairs, recivedPairs,f"API did not return all records correctly")

    """ Testuje czy konfiguracja jest zwracana poprawnie """
    def test_api_returns_configuration(self):
        response = self.client.get(f'/api/v{API_VERSION}/config')
        data =  { 
                "number_of_days":number_of_days,
                "code_length":code_length
                }
        self.assertEqual(data, response.data, f"Did not recive expected values from configuration file")

    def test_api_shows_code(self):
        response = self.client.get(f"/api/v{API_VERSION}/code/{self.link.long_link}",follow=True)
        self.assertEqual(response.data, self.link.code)
@override_settings(SECURE_SSL_REDIRECT=False)
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
    """ Testuje czy usuwane są rekordy z bazy danych """
    def test_api_delete_all_by_treshold(self):
        preDelete = Link.objects.all()
        self.client.delete(f"/api/v{API_VERSION}/short/delete_old")
        postDelete = Link.objects.all()
        self.assertNotEqual(preDelete,postDelete)
@override_settings(SECURE_SSL_REDIRECT=False)
class TestAPIPOSTRequest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user.username = 'demouser'
        self.user.password = 'demodemo'
        self.link = Link.objects.create(
           long_link="https://www.example.com",
            code = "Ex4m" 
        )
        self.url = f"{URL}v{API_VERSION}/short/"
    """ Testuje czy poprawnie jest tworzony link przez zapytanie """
    def test_api_create_new_link(self):
        data = {'long_link':"https://www.example3.com"}
        response = self.client.post(self.url, data, follow=True headers={'Authorization':'Bearer {self.access_token}'})
        print('f3',response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(f"{URL_SHORT}",response.data["code"])
    """ Testuje czy zwracany jest już istniejący link gdy tworzony jest juz w bazie"""
    def test_api_return_existing_link(self):
        data = {'long_link': "https://www.example.com"}
        response = self.client.post(self.url,data, follow=Trueheaders={'Authorization':'Bearer {self.access_token}'})
        print('f4',response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    """ Testuje czy server poprawnie radzi sobie z złym zapytaniem"""
    def test_api_invalid_data(self):
        data = {'long_link':""}
        response = self.client.post(self.url, data, follow=True)
        print('f5',response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("long_link",response.data)
