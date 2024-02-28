from django.urls import path, include

from . import views

app_name = 'api'

urlpatterns = [
    path('products/', views.ProductListApiView.as_view()),
    path('products/<int:pk>', views.ProductDetailAPIView.as_view()),
    # Reviews
    path('reviews/create/', views.ReviewCreateView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
