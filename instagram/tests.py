from django.test import TestCase
from .models import Profile, Image, Likes, Comments
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTestClass(TestCase):
    '''
    Test case for the Profile class and it's behaviours
    '''

    # Set up method
    def setUp(self):
        '''
        Method that will run before any test case under this class
        '''
        self.new_user = User(username = "bilal", email = "bilal@gmail.com", password = "dontbelittleyourself")
        self.new_user.save()

        self.new_profile = Profile(user = self.new_user, bio="self love")

    def tearDown(self):
        Profile.objects.all().delete()

    # Testing instance
    def test_instance(self):
        '''
        Test to confirm that the object is being instantiated correctly
        '''
        self.assertTrue(isinstance(self.new_profile, Profile))