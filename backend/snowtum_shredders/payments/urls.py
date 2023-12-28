# Create urls to append to Project's url
from django.urls import path
from . import views

urlpatterns = [
  path('stripe-payment', views.stripe_payment),
]