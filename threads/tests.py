from django.test import TestCase
from threads.models import *
from django.urls import reverse

# Create your tests here.


def create_thread(**kwargs):
    author = Author.objects.create(
        user_id=kwargs['user_id'], platform_id=kwargs['platform_id'])
    entity = Entity.objects.create(
        entity_id=kwargs['entity_id'], platform_id=kwargs['platform_id'])
    thread = Thread.objects.create(title=kwargs['title'], entity=entity)
    comment = Comment.objects.create(
        author=author, content=kwargs['content'], thread=thread)
    return thread


class ThreadIndexViewTests(TestCase):
    def test_no_thread(self):
        url = reverse('threads:index', args=('serlo', '123'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "[]")
