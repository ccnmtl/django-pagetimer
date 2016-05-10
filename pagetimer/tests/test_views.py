from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from pagetimer.models import PageVisit


class EndpointTest(TestCase):
    def test_not_logged_in(self):
        r = self.client.post(
            reverse('pagetimer-endpoint'),
            dict(path='/something/random'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(PageVisit.objects.count(), 1)
        v = PageVisit.objects.all()[0]
        self.assertEqual(v.username, 'anonymous')
        self.assertEqual(v.path, '/something/random')

    def test_logged_in(self):
        u = User.objects.create(username='testuser')
        u.set_password('password')
        u.save()
        self.client.login(username='testuser', password='password')
        r = self.client.post(
            reverse('pagetimer-endpoint'),
            dict(path='/something/random'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(PageVisit.objects.count(), 1)
        v = PageVisit.objects.all()[0]
        self.assertEqual(v.username, 'testuser')
        self.assertEqual(v.path, '/something/random')


class DashboardTest(TestCase):
    def test_loads(self):
        r = self.client.get(reverse('pagetimer-dashboard'))
        self.assertEqual(r.status_code, 200)


class CSVTest(TestCase):
    def test_loads(self):
        r = self.client.get(reverse('pagetimer-csv'))
        self.assertEqual(r.status_code, 200)
