from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Project


class ProjectLoginRequiredTests(TestCase):
    def test_로그인하지_않으면_등록_화면에_들어갈_수_없다(self):
        response = self.client.get(reverse('project_create'))

        self.assertRedirects(response, f"{reverse('login')}?next=/projects/new/")

    def test_로그인하지_않으면_등록할_수_없다(self):
        self.client.post(reverse('project_create'), {'name': 'investfeed'})

        self.assertFalse(Project.objects.exists())


class ProjectTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user('tester', password='correct-horse-battery')
        self.client.force_login(user)

    def test_프로젝트가_없으면_안내_문구를_보여_준다(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, '아직 등록한 프로젝트가 없습니다.')

    def test_등록하면_저장되고_목록으로_돌아간다(self):
        response = self.client.post(reverse('project_create'), {
            'name': 'investfeed',
            'description': '금융 피드 서비스',
            'stack': 'Spring Boot, React',
        })

        self.assertRedirects(response, reverse('home'))
        project = Project.objects.get()
        self.assertEqual(project.name, 'investfeed')
        self.assertEqual(project.description, '금융 피드 서비스')
        self.assertEqual(project.stack, 'Spring Boot, React')

    def test_이름만_입력해도_등록된다(self):
        self.client.post(reverse('project_create'), {'name': 'purefi'})

        self.assertTrue(Project.objects.filter(name='purefi').exists())

    def test_이름이_없으면_등록되지_않는다(self):
        response = self.client.post(reverse('project_create'), {'name': ''})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.exists())

    def test_이름이_같으면_등록되지_않는다(self):
        Project.objects.create(name='investfeed')

        response = self.client.post(reverse('project_create'), {'name': 'investfeed'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 1)

    def test_목록은_최근_등록한_프로젝트부터_보여_준다(self):
        Project.objects.create(name='먼저 등록')
        Project.objects.create(name='나중 등록')

        response = self.client.get(reverse('home'))

        names = [project.name for project in response.context['project_list']]
        self.assertEqual(names, ['나중 등록', '먼저 등록'])

    def test_입력값의_HTML은_실행되지_않게_바꿔서_보여_준다(self):
        Project.objects.create(name='<b>굵게</b>')

        response = self.client.get(reverse('home'))

        self.assertContains(response, '&lt;b&gt;굵게&lt;/b&gt;')
        self.assertNotContains(response, '<b>굵게</b>')
