from django.test import TestCase
from unittest import mock
from rest_framework.test import APIClient
from rest_framework import status
from .models import Link

class TestLinkModel(TestCase):
    def setUp(self):
        self.link = Link.objects.create(
            long_link="https://www.example.com",
            code = "Ex4mp7e"
        )
    def test_link_create(self):
        self.assertEqual(self.link.long_link, "https://www.example.com")
        self.assertTrue(self.link.code)
        self.assertIsNotNone(self.link.lastUsed)
    
    def test_link_create_raises_exception(self):
        with self.assertRaises(Exception):
            Link.objects.create(
                long_link = "https://www.example.com",
                code="Ex4mp7e"
            )
    