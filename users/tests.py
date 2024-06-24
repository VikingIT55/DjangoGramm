from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='S0m3C0mpl3xP@ssw0rd!')

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.first_name, '')
        self.assertEqual(profile.last_name, '')
        self.assertEqual(profile.bio, '')


class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='S0m3C0mpl3xP@ssw0rd!')

    def test_register_view_get(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_password_complexity(self):
        response = self.client.post(reverse('users:register'),
                                    {'username': 'testpassword',
                                        'email': 'test@gmail.com',
                                        'password1': 'testtest',
                                        'password2': 'testtest'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is too common.", html=True)
        self.assertFalse(User.objects.filter(username='testpassword').exists())

    def test_register_view_post(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'S0m3C0mpl3xP@ssw0rd!',
            'password2': 'S0m3C0mpl3xP@ssw0rd!'
        })
        self.assertEqual(response.status_code, 302, msg="Registration should result in a redirect")
        self.assertRedirects(response, reverse('users:configurate'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'S0m3C0mpl3xP@ssw0rd!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:profile', kwargs={'username': 'testuser'}))

    def test_logout_view(self):
        self.client.login(username='testuser', password='S0m3C0mpl3xP@ssw0rd!')
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_configurate_view_get(self):
        self.client.login(username='testuser', password='S0m3C0mpl3xP@ssw0rd!')
        response = self.client.get(reverse('users:configurate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/configurate_page.html')

    def test_configurate_view_post(self):
        self.client.login(username='testuser', password='S0m3C0mpl3xP@ssw0rd!')
        response = self.client.post(reverse('users:configurate'), {
            'first_name': 'Updated',
            'last_name': 'User',
            'bio': 'Updated bio'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:profile', kwargs={'username': 'testuser'}))
        profile = Profile.objects.get(user=self.user)
        profile.refresh_from_db()
        self.assertEqual(profile.first_name, 'Updated')
        self.assertEqual(profile.bio, 'Updated bio')

    def test_profile_view(self):
        self.client.login(username='testuser', password='S0m3C0mpl3xP@ssw0rd!')
        response = self.client.get(reverse('users:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
