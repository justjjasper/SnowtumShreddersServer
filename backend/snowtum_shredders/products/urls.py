# Create urls to append to Project's url
from django.urls import path
from . import views

urlpatterns = [
  path('megasnowboards/', views.mega_snowboards),
  path('collections', views.get_product_collections),
  path('snowboards', views.get_snowboard_collection),
  path('accessories', views.get_accessory_collection),
  path('snowboard/<str:snowboard_name>', views.get_snowboard_product),
  path('tshirt/<str:tshirt_name>', views.get_tshirt_product),
  path('hoodie/<str:hoodie_name>', views.get_hoodie_product),
  path('headgear/<str:headgear_name>', views.get_headgear_product),
  path('boardbag/<str:boardbag_name>', views.get_boardbag_product),
  path('post_review', views.post_review)
]