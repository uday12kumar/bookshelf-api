import os
from unittest import mock

import boto3
from django.test import TestCase
from moto import mock_sns
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from bookshelf.books.tests.factories import GenreFactory, BookFactory
from bookshelf.books.models import Genre, Book


class BookTestCase(TestCase):
    """ Test module for Book model """

    def setUp(self):
        self.book = BookFactory()

    def test_book_object(self):
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().genre.count(), 1)
        self.assertEqual(Book.objects.first().author.count(), 1)


class GenreTestCase(APITestCase):
    api_ = """ Test module for Genre model"""

    def setUp(self):
        self.author = GenreFactory.create_batch(size=50)

    def test_genre(self):
        self.assertEqual(Genre.objects.count(), 50)
