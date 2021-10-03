from django.contrib.auth import get_user_model
from django.test import TestCase
from allauth.account.models import EmailAddress

class LandPageTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test1',
            email='test1@edu.osakafu-u.ac.jp',
            password='psst1'
        )

    def test_get_success_when_unauthenticated(self):
        EmailAddress.objects.create(
            user=self.user,
            email="test1@edu.osakafu-u.ac.jp",
            primary=True,
            verified=False,
        )
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_success_when_logged_in(self):
        logged_in = self.client.login(username=self.user.username, password='psst1')
        self.assertTrue(logged_in)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_success_when_logged_out(self):
        self.client.logout()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class TopPageTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test1',
            email='test1@edu.osakafu-u.ac.jp',
            password='psst1'
        )

    def test_redirect_when_unauthenticated(self):
        EmailAddress.objects.create(
            user=self.user,
            email="test1@edu.osakafu-u.ac.jp",
            primary=True,
            verified=False,
        )
        response = self.client.get('/top_page/')
        self.assertRedirects(response, '/accounts/login/?next=/top_page/')

    def test_get_success_when_logged_in(self):
        logged_in = self.client.login(username=self.user.username, password='psst1')
        self.assertTrue(logged_in)
        response = self.client.get('/top_page/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_when_logged_out(self):
        self.client.logout()
        response = self.client.get('/top_page/')
        self.assertRedirects(response, '/accounts/login/?next=/top_page/')


"""
AccountTests
EmailFormTests
BaseSignupFormTests
CustomSignupFormTests
AuthenticationBackendTests
UtilsTests
ConfirmationViewTests
ConfirmationViewTests
TestCVE2019_19844
RequestAjaxTests
"""