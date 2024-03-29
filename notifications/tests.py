import shutil
import tempfile
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase
from posts.models import Post, Comment, CommentLikes
from users.models import Profile

from .models import Notification
from .mentions import check_instance

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
        Notification.objects.create(
            sender=test,
            recipient=admin,
            text='test commented: "Sick that mate."',
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
        response = self.client.post(
            f'/api/notifications/read/{notification.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue(
            Notification.objects.filter(
            text='test liked your post.',
            read=True
        ).exists())

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
        response = self.client.post(
            f'/api/notifications/unread/{notification.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(200, response.status_code)
        self.assertTrue(
            Notification.objects.filter(
            text='test liked your post.',
            read=False
        ).exists())

    def mark_all_as_read(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            }
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/notifications/read/all/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(Notification.objects.filter(
            read=True
        ).count(), 2)

    def get_all_notifications(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            }
        )
        access_token = access_request.data['access']
        response = self.client.get(
            '/api/notifications/all/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def get_all_notifications_unauthorised(self):
        response = self.client.get(
            '/api/notifications/all/'
        )
        self.assertEqual(response.status_code, 401)

    def get_notification(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            }
        )
        access_token = access_request.data['access']
        notification = Notification.objects.get(
            text='test liked your post.',
            target_object_id=1
        )
        response = self.client.get(
            f'/api/notifications/{notification.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def get_notification_404(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': '5up3R!97'
            }
        )
        access_token = access_request.data['access']
        response = self.client.get(
            '/api/notifications/105/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 404)

    def test_in_order(self):
        self.mark_notification_as_read()
        self.mark_notification_as_unread()
        self.mark_all_as_read()
        self.get_all_notifications()
        self.get_all_notifications_unauthorised()
        self.get_notification()
        self.get_notification_404()

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

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestMentions(APITestCase):
    def setUp(self):
        Profile.objects.create(
            username="admin",
            email="matt@mspe.me",
            password=make_password("5up3R!97")
        )
        profile = Profile.objects.get(username='admin')
        Post.objects.create(
            author= profile,
            image=SimpleUploadedFile('test.png', b'testimage'),
            description='Test'
        ).save()
        post = Post.objects.get(description='Test')
        Comment.objects.create(
            author=profile,
            post=post,
            content='Cool post.'
        ).save()
        comment = Comment.objects.get(content='Cool post.')
        CommentLikes.objects.create(
            comment=comment,
            profile=profile
        ).save()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_check_instance_post_working(self):
        post = Post.objects.get(description='Test')
        response = check_instance(post)
        self.assertEqual(response, 'admin')

    def test_check_instance_comment_working(self):
        comment = Comment.objects.get(content='Cool post.')
        response = check_instance(comment)
        self.assertEqual(response, 'admin')

    def test_check_instance_exception(self):
        commentlike = CommentLikes.objects.get(comment__content='Cool post.')
        with self.assertRaises(Exception):
            check_instance(commentlike)
