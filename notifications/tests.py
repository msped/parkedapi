import shutil
import tempfile
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase
from posts.models import Post
from users.models import Profile

from .models import Notification

MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestViews(APITestCase):
    def setUp(self):
        Profile.objects.create(
            username="admin",
            email="matt@mspe.me",
            password=make_password("5up3R!97")
        )
        Profile.objects.create(
            username="test",
            email="test@mspe.me",
            password=make_password("5up3R!98")
        )
        profile = Profile.objects.get(username='admin')
        Post.objects.create(
            author= profile,
            image=SimpleUploadedFile('test.png', b'testimage'),
            description='Test'
        ).save()

        admin = Profile.objects.get(username='admin')
        test = Profile.objects.get(username='test')

        c_type = ContentType.objects.get(app_label='posts', model='post')
        Notification.objects.create(
            sender=test,
            recipient=admin,
            text='test liked your post.',
            target_content_type=c_type,
            target_object_id=1
        ).save()


    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def mark_notification_as_read(self):
        notification = Notification.objects.get(
            text='test liked your post.'
        )
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            }
        )
        access_token = access_request.data['access']
        response = self.client.get(
            f'/api/notifications/read/{notification.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(200, response.status_code)

    def mark_notification_as_unread(self):
        notification = Notification.objects.get(
            text='test liked your post.'
        )
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            }
        )
        access_token = access_request.data['access']
        response = self.client.get(
            f'/api/notifications/unread/{notification.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(200, response.status_code)

    def test_in_order(self):
        self.mark_notification_as_read()
        self.mark_notification_as_unread()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestModels(APITestCase):
    def setUp(self):
        Profile.objects.create(
            username="admin",
            email="matt@mspe.me",
            password=make_password("5up3R!97")
        )
        Profile.objects.create(
            username="test",
            email="test@mspe.me",
            password=make_password("5up3R!98")
        )
        profile = Profile.objects.get(username='admin')
        Post.objects.create(
            author= profile,
            image=SimpleUploadedFile('test.png', b'testimage'),
            description='Test'
        ).save()

        admin = Profile.objects.get(username='admin')
        test = Profile.objects.get(username='test')

        c_type = ContentType.objects.get(app_label='posts', model='post')
        Notification.objects.create(
            sender=test,
            recipient=admin,
            text='test liked your post.',
            target_content_type=c_type,
            target_object_id=1
        ).save()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_str(self):
        notification = Notification.objects.get(
            text='test liked your post.'
        )
        self.assertEqual(
            str(notification),
            'Sent to admin - Read: False'
        )
