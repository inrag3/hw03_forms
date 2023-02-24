from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from ..models import Group, Post
from django.urls import reverse

User = get_user_model()


class PostViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_posts_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': PostViewTest.group.slug}):
            'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': PostViewTest.user.username}):
            'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': PostViewTest.post.id}):
            'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': PostViewTest.post.id}):
            'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test',
            description='Тестовое описание',
        )
        cls.post = [
            Post.objects.create(
                text='Тестовый пост',
                author=PaginatorViewsTest.user,
                group=PaginatorViewsTest.group,
            )
            for _ in range(13)
        ]

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_posts_pages_contains_necessary_records(self):
        first_page = 10
        second_page = 3
        pages_len = {
            reverse('posts:index'): first_page,
            reverse('posts:index') + '?page=2': second_page,
            reverse('posts:group_list',
                    kwargs={'slug': PaginatorViewsTest.group.slug}):
            first_page,
            reverse('posts:group_list', kwargs={
                    'slug': PaginatorViewsTest.group.slug}) + '?page=2':
            second_page,
            reverse('posts:profile',
                    kwargs={'username': PaginatorViewsTest.user.username}):
            first_page,
            reverse('posts:profile', kwargs={
                    'username': PaginatorViewsTest.user.username}) + '?page=2':
            second_page,
        }
        for reverse_page, posts_len in pages_len.items():
            response = self.authorized_client.get(reverse_page)
            with self.subTest(reverse_page=reverse_page):
                self.assertEqual(len(response.context['page_obj']), posts_len)
