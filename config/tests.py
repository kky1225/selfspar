from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginTests(TestCase):
    def setUp(self):
        self.username = 'tester'
        self.password = 'correct-horse-battery'
        get_user_model().objects.create_user(self.username, password=self.password)

    def login(self, password):
        return self.client.post(
            reverse('login'),
            {'username': self.username, 'password': password},
        )

    def test_로그인하지_않으면_홈에서_로그인_화면으로_보낸다(self):
        response = self.client.get(reverse('home'))

        self.assertRedirects(response, f"{reverse('login')}?next=/")

    def test_로그인_화면은_로그인_없이_열린다(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)

    def test_비밀번호가_틀리면_로그인되지_않는다(self):
        response = self.login('wrong-password')

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_로그인하면_홈으로_간다(self):
        response = self.login(self.password)

        self.assertRedirects(response, reverse('home'))

    def test_로그아웃하면_홈에_다시_들어갈_수_없다(self):
        self.login(self.password)

        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

        response = self.client.get(reverse('home'))
        self.assertRedirects(response, f"{reverse('login')}?next=/")

    def test_로그아웃은_GET_요청으로_되지_않는다(self):
        self.login(self.password)

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)
