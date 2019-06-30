from django.test import TestCase

# Create your tests here.

class BaseTestClass(TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_something_that_will_pass(self):
        self.assertFalse(False)

    def test_something_that_will_fail(self):
        self.assertTrue(False)
