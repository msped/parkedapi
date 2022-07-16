import json

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Profile

# Create your tests here.

class AuthTests(APITestCase):

    def setUp(self):
        Profile.objects.create(
            username="admin",
            email="matt@mspe.me",
            password=make_password("5up3R!97")
        )

    def registration_working_response(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'test',
                'email': 'test@gmail.com',
                'password': '5up3R!98',
                'password2': '5up3R!98'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def registration_invalid_username(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': '',
                'email': 'test2@gmail.com',
                'password': '5up3R!98',
                'password2': '5up3R!98'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "username": ["This field may not be blank."]
            }
        )

    def registration_invalid_email(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'test2',
                'email': 'test2gmail.com',
                'password': '5up3R!98',
                'password2': '5up3R!98'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "email": ["Enter a valid email address."]
            }
        )

    def registration_passwords_dont_match(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'test3',
                'email': 'test3@gmail.com',
                'password': '5up4R!98',
                'password2': '5up4R!97'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "password": ["Password fields don't match"]
            }
        )

    def request_access_token(self):
        response = self.client.post(
            '/api/auth/token/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def request_refresh_token(self):
        access_request = self.client.post(
            '/api/auth/token/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            },
            format='json'
        )
        refresh_token = access_request.data['refresh']
        response = self.client.post(
            '/api/auth/token/refresh/',
            {
                'username': 'admin',
                'password': '5up3R!97',
                'refresh': refresh_token
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def blacklist_token(self):
        access_request = self.client.post(
            '/api/auth/token/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            },
            format='json'
        )
        refresh_token = access_request.data['refresh']
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/auth/token/blacklist/',
            {
                'refresh': refresh_token
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def change_password_check_new_and_old(self):
        profile = Profile.objects.get(username='admin')
        access_request = self.client.post(
            '/api/auth/token/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            f'/api/auth/change-password/{profile.id}/',
            {
                'old_password': '5up3R!97',
                'new_password': '5up3R!97',
                'new_password2': '5up3R!97'
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 400)

    def change_password_wrong_old_password(self):
        profile = Profile.objects.get(username='admin')
        access_request = self.client.post(
            '/api/auth/token/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            f'/api/auth/change-password/{profile.id}/',
            {
                'old_password': '5up3R!99',
                'new_password': '5up3R!00',
                'new_password2': '5up3R!00'
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 400)

    def change_password_new_not_matching(self):
        profile = Profile.objects.get(username='admin')
        access_request = self.client.post(
            '/api/auth/token/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            f'/api/auth/change-password/{profile.id}/',
            {
                'old_password': '5up3R!97',
                'new_password': '5up3R!14',
                'new_password2': '5up3R!83'
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 400)

    def change_password_valid(self):
        profile = Profile.objects.get(username='admin')
        access_request = self.client.post(
            '/api/auth/token/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            f'/api/auth/change-password/{profile.id}/',
            {
                'old_password': '5up3R!97',
                'new_password': '5up3R!00',
                'new_password2': '5up3R!00'
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_in_order(self):
        self.registration_working_response()
        self.registration_invalid_username()
        self.registration_invalid_email()
        self.registration_passwords_dont_match()
        self.request_access_token()
        self.request_refresh_token()
        self.blacklist_token()
        self.change_password_check_new_and_old()
        self.change_password_new_not_matching()
        self.change_password_wrong_old_password()
        self.change_password_valid()
