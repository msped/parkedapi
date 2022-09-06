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
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        post = Post.objects.get(description='Test image of car')
        response = self.client.post(
            f'/api/posts/like/{post.slug}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def post_unlike(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        post = Post.objects.get(description='Test image of car')
        response = self.client.post(
            f'/api/posts/like/{post.slug}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def new_comment(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        post = Post.objects.get(description='Test image of car')
        response = self.client.post(
            f'/api/posts/{post.slug}/comment/new/',
            {
                'content': 'This is a cool comment.'
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def comment_like(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        comment = Comment.objects.get(content='This is a cool comment.')
        response = self.client.post(
            f'/api/posts/comment/like/{comment.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def comment_unlike(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        comment = Comment.objects.get(content='This is a cool comment.')
        response = self.client.post(
            f'/api/posts/comment/like/{comment.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def update_comment(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        comment = Comment.objects.get(content='This is a cool comment.')
        response = self.client.patch(
            f'/api/posts/comment/{comment.id}/',
            {
                'content': 'This is an awesome comment.'
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def delete_comment(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        comment = Comment.objects.get(content='This is an awesome comment.')
        response = self.client.delete(
            f'/api/posts/comment/{comment.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def update_post(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        post = Post.objects.get(description='Test image of car')
        response = self.client.patch(
            f'/api/posts/{post.slug}/',
            {
                'description': 'Test description of car'
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_post(self):
        access_request = self.client.post(
            '/api/auth/jwt/create/',
            {
                'username': 'admin',
                'password': 'TestP455word!'
            }
        )
        access_token = access_request.data['access']
        post = Post.objects.get(description='Test description of car')
        response = self.client.delete(
            f'/api/posts/{post.slug}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_in_order(self):
        self.new_post()
        self.post_like()
        self.post_unlike()
        self.new_comment()
        self.comment_like()
        self.comment_unlike()
        self.update_comment()
        self.delete_comment()
        self.update_post()
        self.delete_post()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestModels(APITestCase):
    def setUp(self):
        profile = Profile.objects.create(
            first_name= 'Harold',
            last_name= 'Finch',
            username= 'admin',
            password=make_password('TestP455word!')
        )
        profile.save()

        profile_2 = Profile.objects.create(
            first_name= 'John',
            last_name= 'Reese',
            username= 'asset',
            password=make_password('TestP455word!')
        )
        profile_2.save()

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

    def post_str(self):
        profile = Profile.objects.get(username='admin')
        new_post = Post.objects.create(
            author= profile,
            image=SimpleUploadedFile('test.png', b'testimage'),
            description='Test'
        )
        new_post.save()
        post = Post.objects.get(description='Test')
        self.assertEqual(str(post), f'admin - {new_post.created_at}')

    def post_likes_str(self):
        post = Post.objects.get(description='Test')
        profile = Profile.objects.get(username='asset')
        post_like = PostLikes.objects.create(
            post=post,
            profile=profile
        )
        post_like.save()
        like_instance = PostLikes.objects.get(
            profile_id=profile.id,
            post_id=post.id
        )
        self.assertEqual(str(like_instance), "asset likes admin's post")

    def comment_str(self):
        post = Post.objects.get(description='Test')
        profile = Profile.objects.get(username='asset')
        com = Comment.objects.create(
            profile=profile,
            post=post,
            content='Cool post.'
        )
        com.save()
        comment = Comment.objects.get(content='Cool post.')
        self.assertEqual(str(comment), f'asset - admin - {post.created_at}')

    def comment_likes_str(self):
        profile = Profile.objects.get(username='admin')
        comment = Comment.objects.get(content='Cool post.')
        comment_like = CommentLikes.objects.create(
            comment=comment,
            profile=profile
        )
        comment_like.save()
        like_instance = CommentLikes.objects.get(
            profile_id=profile.id,
            comment_id=comment.id
        )
        self.assertEqual(str(like_instance), "admin likes asset's comment")

    def post_comment_count(self):
        post = Post.objects.get(description='Test')
        self.assertEqual(post.get_comment_count(), 1)

    def post_like_count(self):
        post = Post.objects.get(description='Test')
        self.assertEqual(post.get_likes_count(), 1)

    def comment_likes_count(self):
        comment = Comment.objects.get(content='Cool post.')
        self.assertEqual(comment.get_likes_count(), 1)

    def test_in_order(self):
        self.post_str()
        self.post_likes_str()
        self.comment_str()
        self.comment_likes_str()
        self.post_comment_count()
        self.post_like_count()
        self.comment_likes_count()
