from django.test import TestCase

# Create your tests here.
from .models import Book
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class ModelTestCase(TestCase):
    def setUp(self):
        self.book = Book(name="Thinking in Python")

    def test_model_can_create_a_book(self):
        old_count = Book.objects.count()
        self.book.save()
        new_count = Book.objects.count()
        self.assertEqual(old_count + 1, new_count)


class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.book_data = {'name': 'Thinking in java'}
        self.response = self.client.post(
            reverse('create'), self.book_data, format="json")

    def test_api_can_create_a_book(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_book(self):
        """Test the api can get a given book."""
        book = Book.objects.get()
        response = self.client.get(
            reverse('details', kwargs={'pk': book.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, book)

    def test_api_can_update_book(self):
        """Test the api can update a given book."""
        book = Book.objects.get()
        change_book = {'name': 'Thinking in php'}
        res = self.client.put(
            reverse('details', kwargs={'pk': book.id}),
            change_book,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_book(self):
        """Test the api can delete a book."""
        book = Book.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': book.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
