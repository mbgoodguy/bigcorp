from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# from validators import ValidationError  # will not show error in Postman when send more than 1 review by POST to http://127.0.0.1:8000/api/reviews/create/
from rest_framework.exceptions import ValidationError


from recommend.models import Review
from .pagination import StandardResultsSetPagination
from .permissions import IsAdminOrReadOnly
from .serializers import ProductSerializer, ProductDetailSerializer, ReviewSerializer
from shop.models import Product, Category


class ProductListApiView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').order_by('id')


class ProductDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.select_related('category').order_by('id')


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        existing_review = Review.objects.filter(product=product, created_by=self.request.user).exists()
        if existing_review:
            raise ValidationError('You have already reviewed this product.')

        serializer.save(created_by=self.request.user, product=product)
