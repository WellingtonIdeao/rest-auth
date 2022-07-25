from django.test import TestCase, RequestFactory
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from ..views import UserLoginView, UserLogoutView, UserViewSet


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


class UserLogoutViewTest(TestCase):
    fixtures = ['user.json']

    def test_logout_url_location(self):
        response = self.client.get('/api-auth/logout/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url_location_by_namespace(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_logout_template_used_is_correct(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/registration/logged_out.html')

    def test_logout_template_used_is_correct_by_view(self):
        request = RequestFactory().get(reverse('logout'))
        view = UserLogoutView()
        view.setup(request)
        templates_names = view.get_template_names()
        self.assertIn('api/registration/logged_out.html', templates_names)

    def test_logout_url_name(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.url_name, 'logout')

    def test_logout_view_served_the_response(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, UserLogoutView)

    def test_logout_auth_user(self):
        # Login the user
        logged_in = self.client.login(username='admin', password='123456')
        self.assertTrue(logged_in)

        # Logout the user
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

        # Check if user is logout
        user = response.context['user']
        is_auth = user.is_authenticated
        self.assertFalse(is_auth)

    def test_logout_title_is_in_context_by_view(self):
        request = RequestFactory().get(reverse('logout'))
        view = UserLogoutView()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn('title', context)

    def test_logout_title_is_in_context_by_req_resp_cycle(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

        self.assertTrue('title' in response.context)


class UserViewSetTest(APITestCase):
    fixtures = ['user.json']

    def test_get_list_users_by_url_location(self):
        url = '/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_users_by_url_namespace(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_user_by_url_location(self):
        url = '/users/1/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_user_by_url_namespace(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_user_url_json_format(self):
        url = '/users.json'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_url_json_format(self):
        url = '/users/1.json'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_user_length(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)

    def test_get_list_response_data(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, [{'url': 'http://testserver/users/1/', 'id': 1, 'username': 'admin'}])

    def test_get_list_rendered(self):
        view = UserViewSet.as_view({'get': 'list'})
        url = reverse('user-list')
        request = APIRequestFactory().get(url)
        response = view(request)
        response.render()
        self.assertEqual(response.content, b'[{"url":"http://testserver/users/1/","id":1,"username":"admin"}]')

    def test_get_detail_response_data(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')

        domain = 'http://testserver'
        self.assertEqual(response.data, {'url': domain+url, 'id': 1, 'username': 'admin'})

    def test_get_detail_rendered(self):
        view = UserViewSet.as_view({'get': 'retrieve'})
        url = reverse('user-detail', kwargs={'pk': 1})
        request = APIRequestFactory().get(url)
        response = view(request, pk=1)
        response.render()
        self.assertEqual(response.content, b'{"url":"http://testserver/users/1/","id":1,"username":"admin"}')

