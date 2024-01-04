import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Product, Category, ProductProxy


class ProductViewTest(TestCase):
    def tearDown(self):
        # delete temp files after test
        for product in Product.objects.all():
            if product.image:
                os.remove(product.image.path)

    def test_get_products(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='django')
        product_1 = Product.objects.create(title='Product 1', category=category, image=uploaded, slug='product-1')
        product_2 = Product.objects.create(title='Product 2', category=category, image=uploaded, slug='product-2')

        response = self.client.get(reverse('shop:products'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), 2)
        self.assertEqual(list(response.context['products']), [product_1, product_2])
        self.assertContains(response, product_1.title)
        self.assertContains(response, product_2.title)


class CategoryListViewTest(TestCase):
    def tearDown(self):
        # Удаляем временные файлы после завершения теста
        for product in Product.objects.all():
            if product.image:
                os.remove(product.image.path)

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(
            name='Test Category', slug='test-category'
        )
        self.product = Product.objects.create(
            title='Test Product', slug='test-product', category=self.category, image=uploaded
        )

    def test_status_code(self):
        response = self.client.get(
            reverse('shop:category_list', args=[self.category.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse('shop:category_list', args=[self.category.slug])
        )
        self.assertTemplateUsed(response, 'shop/category_list.html')

    def test_context_data(self):
        response = self.client.get(
            reverse('shop:category_list', args=[self.category.slug])
        )
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)
