from django.urls import path
from ..views import CriarProdutoView

urlpatterns = [
    path('criar/', CriarProdutoView.as_view(), name='criar-produto'),
]
