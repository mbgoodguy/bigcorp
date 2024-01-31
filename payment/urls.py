import stripe
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from . import views
from .webhooks import stripe_webhook

app_name = 'payment'

urlpatterns = [
    path('shipping/', views.shipping, name='shipping'),
    path('checkout/', views.checkout, name='checkout'),
    path('complete_order/', views.complete_order, name='complete-order'),
    path('payment_success/', views.payment_success, name='payment-success'),
    path('payment_fail/', views.payment_fail, name='payment-fail'),
    path('webhook_stripe/', stripe_webhook, name='webhook-stripe'),

]
