from django.test import TestCase
# we can use this or do it in pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Contact
from django.test.client import Client
from django.contrib.auth.models import User
import json
from .serializers import ContactMessageSerializer

class MessageViewSetTest(APITestCase):
    def setUp(self) -> None:

        self.admin_user = Client()
        self.base_user = Client()

        self.user = User.objects.create_superuser(
            username='foobar',
            email='foo@bar.com',
            password='hatefoobarpeople')

        self.admin_user.force_login(user=self.user)

        self.message_dummy = {
            'name': 'Marcel Czuryszkiewicz',
            'email': 'czuryszkiewicz@domain.com',
            'subject': 'app',
            'message': 'one test please'
        }
        # Should be contained in some sort of json file to be read from


    def test_get_messages_admin(self):

        response = self.admin_user.get(reverse('message-list'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_messages_all(self):

        response = self.base_user.get(reverse('message-list'))
        self.assertEqual(response.status_code, 403)

    def test_post_correct_payload(self):

        response_base = self.base_user.post(reverse('message-list'), self.message_dummy)
        response_admin = self.admin_user.post(reverse('message-list'), self.message_dummy)
  
        self.assertEqual(response_base.status_code, 201)
        # Should be separated or generified - cases for admin and for base user
        # Try separated test-cases for each type of role
        self.assertEqual(response_admin.status_code, 201)
        self.assertEqual(response_admin.data['name'], self.message_dummy['name'])

    def test_post_incorrect_payload(self):

        self.message_dummy['subject'] = "this cant work"

        response_base = self.base_user.post(reverse('message-list'), self.message_dummy)
        response_admin = self.admin_user.post(reverse('message-list'), self.message_dummy)
        # Should be separated or generified - cases for admin and for base user
        # Try separated test-cases for each type of role
        self.assertEqual(response_base.status_code, 400)
        self.assertEqual(response_admin.status_code, 400)
        

    """
    We can test serializers to but in this case I don't think that's necessary
    because we are doing full request-response cycle
    Regardles of that here is one for fun
    """

    def test_email_valid(self):
        
        self.message_dummy['email'] = 'emaildomain.com'
        serializer = ContactMessageSerializer(data=self.message_dummy)
        #FIXME: This test does not actually check only whether the email is valid - it calls is_valid on serializer, which uses validate() implementation inside it
        # this implementation validates more than just email, so is it actually a check if only the email is valid?
        # What's more - the email check is done by internal Django function - there is no apparent reason to check if something what's already tested is working well.
        # This test-case is flawed and kind of useless.
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['Invalid Email']))
