from django.core.urlresolvers import reverse
from django.test import TestCase
from pagetimer.models import PageVisit


class SimpleTest(TestCase):
    def test_not_logged_in(self):
        r = self.client.post(
            reverse('pagetimer-endpoint'),
            dict(path='/something/random'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(PageVisit.objects.count(), 1)
        v = PageVisit.objects.all()[0]
        self.assertEqual(v.username, 'anonymous')
        self.assertEqual(v.path, '/something/random')
