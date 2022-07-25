from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from ..views import UserLoginView


class UserLoginViewTest(TestCase):
    fixtures = ['user.json']

    def test_login_url_location(self):
        response = self.client.get('/api-auth/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_location_by_namespace(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_template_used_is_correct(self):
        request = RequestFactory().get(reverse('login'))
        response = UserLoginView.as_view()(request)

        with self.assertTemplateUsed('api/registration/login.html'):
            response.render()

    def test_login_url_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'login')

    def test_login_view_served_the_response(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, UserLoginView)

    def test_logged_in_user_browser_was_successful(self):
        # Setting user on client(browser)
        logged_in = self.client.login(username='admin', password='123456')

        # logged_in is True if the credentials were accepted and login was successful.
        self.assertTrue(logged_in)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'admin')

    def test_logged_in_user_was_successful_by_post_request(self):
        response = self.client.post(reverse('login'), data={'username': 'admin', 'password': '123456'}, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'admin')

    def test_redirect_to_correct_page_after_login(self):
        response = self.client.post(reverse('login'), data={'username': 'admin', 'password': '123456'}, follow=True)
        self.assertEqual(response.status_code, 200)

        # checks if redirect to correct page after the user logged in.
        self.assertRedirects(response, expected_url=reverse('admin:index'))

    def test_form_is_in_context(self):
        request = RequestFactory().get(reverse('login'))
        view = UserLoginView()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn('form', context)

    def test_form_is_authentication_form(self):
        request = RequestFactory().get(reverse('login'))
        view = UserLoginView()
        view.setup(request)
        form = view.form_class
        self.assertEqual(form, AuthenticationForm)

    def test_user_is_not_authenticated(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        user = response.context['user']
        is_auth = user.is_authenticated
        self.assertFalse(is_auth)

