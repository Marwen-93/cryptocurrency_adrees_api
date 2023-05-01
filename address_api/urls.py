from django.urls import path
# from .views import ListRetriveCryptoCurrencyView ,CryptoCurrencyView
from . import views

urlpatterns = [
    path('generate/', views.generate_address),
    path('list/', views.list_address),
    path('retrieve/<int:pk>/', views.retrieve_address),
]
