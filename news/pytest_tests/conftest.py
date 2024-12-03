from datetime import timezone, timedelta

import pytest

from django.test.client import Client

from news.models import News
from yanews import settings


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='GenkoNide')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='NotGenkoNide')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def new_post(author):
    date_now = timezone.now()
    post_author = News.objects.create(
        title='Заголовок новости, автором которой будет GenkoNide',
        text='Текст заметки',
        author=author,
        date=date_now,
    )
    return post_author

@pytest.fixture
def news_post_list():
    """Создает новости для тестирования."""
    date_now = timezone.now()
    news_count = settings.NEWS_COUNT_ON_HOME_PAGE + 1
    news_items = [
        News(title=f'Заголовок {i}',
             text='Текст',
             date=date_now - timedelta(days=i)
             )
        for i in range(news_count)
    ]
    News.objects.bulk_create(news_items)