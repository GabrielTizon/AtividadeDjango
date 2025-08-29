from django.urls import path
from . import views

urlpatterns = [
    # Produtos
    path("", views.product_list, name="product_list"),
    path("<int:pk>/", views.product_detail, name="product_detail"),

    # Carrinho
    path("carrinho/", views.cart_detail, name="cart_detail"),
    path("carrinho/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("carrinho/update/<int:product_id>/", views.update_cart_item, name="update_cart_item"),
    path("carrinho/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("carrinho/limpar/", views.clear_cart, name="clear_cart"),
]
