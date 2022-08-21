import shutil
import tempfile

from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Profile

from .apps import PostsConfig
from .models import Comment, CommentLikes, Post, PostLikes

MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)

class TestPostApp(APITestCase):

    def setUp(self):
        profile = Profile.objects.create(
            first_name= 'Harold',
            last_name= 'Finch',
            username= 'admin',
            password=make_password('TestP455word!')
        )
        profile.save()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def temporary_image(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, 'jpeg')
        tmp_file.seek(0)
        return tmp_file

    def test_app_config(self):
        self.assertEqual('posts', PostsConfig.name)

    def new_post(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/posts/new/',
            {
                'image': self.temporary_image(),
                'description': 'Test image of car',
                'comments_enabled': True,
            },
            format='multipart',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def post_like(self):
        pass

    def post_unlike(self):
        pass

    def new_comment(self):
        pass

    def comment_like(self):
        pass

    def comment_unlike(self):
        pass

    def delete_comment(self):
        pass

    def delete_post(self):
        pass

    def test_in_order(self):
        self.new_post()
