from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ProductAPITests(APITestCase):
    def test_list_products(self):
        """
        Ensure we can list all products.
        """
        url = reverse('product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
