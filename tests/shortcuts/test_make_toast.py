from django.shortcuts import make_toast
from django.test import SimpleTestCase

# This test ensures that make_toast() returns "toast"
class MakeToastTests(SimpleTestCase):
    def test_make_toast(self):
        self.assertEqual(make_toast(), "toast")