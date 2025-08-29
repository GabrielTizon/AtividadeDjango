from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Product

# ---------------------------
# Produtos (lista e detalhe)
# ---------------------------

def product_list(request):
    """
    Lista os 5 produtos mais recentes.
    Ajuste/retire o [:5] se quiser listar todos.
    """
    latest_product_list = Product.objects.order_by("-pub_date")[:5]
    return render(request, "store/index.html", {"latest_product_list": latest_product_list})


def product_detail(request, pk):
    """
    Página de detalhe do produto.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/detail.html", {"product": product})


# ---------------------------
# Carrinho (armazenado na sessão)
# ---------------------------

CART_SESSION_KEY = "cart"  # dict: { "product_id": qty }


def _get_cart(request):
    return request.session.get(CART_SESSION_KEY, {})


def _save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


@require_POST
def add_to_cart(request, product_id: int):
    """
    Adiciona um produto ao carrinho (qty padrão = 1).
    """
    product = get_object_or_404(Product, pk=product_id)
    try:
        qty = int(request.POST.get("qty", 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(1, min(qty, 999))

    cart = _get_cart(request)
    key = str(product_id)
    cart[key] = cart.get(key, 0) + qty
    _save_cart(request, cart)
    messages.success(request, f'"{product.name}" adicionado ao carrinho.')
    return redirect("cart_detail")


def cart_detail(request):
    """
    Página do carrinho: lista itens, totais, etc.
    """
    cart = _get_cart(request)
    ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=ids)

    items = []
    total = Decimal("0.00")
    for p in products:
        qty = int(cart.get(str(p.id), 0))
        subtotal = (p.price or Decimal("0.00")) * qty
        total += subtotal
        items.append({"product": p, "qty": qty, "subtotal": subtotal})

    context = {
        "items": items,
        "total": total,
        "total_qty": sum(cart.values()) if cart else 0,
    }
    return render(request, "store/cart.html", context)


@require_POST
def update_cart_item(request, product_id: int):
    """
    Atualiza a quantidade de um item do carrinho (0 remove).
    """
    product = get_object_or_404(Product, pk=product_id)
    try:
        qty = int(request.POST.get("qty", 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(0, min(qty, 999))

    cart = _get_cart(request)
    key = str(product_id)
    if qty <= 0:
        cart.pop(key, None)
        messages.info(request, f'"{product.name}" removido do carrinho.')
    else:
        cart[key] = qty
        messages.success(request, f'Quantidade de "{product.name}" atualizada para {qty}.')
    _save_cart(request, cart)
    return redirect("cart_detail")


@require_POST
def remove_from_cart(request, product_id: int):
    """
    Remove um item do carrinho.
    """
    product = get_object_or_404(Product, pk=product_id)
    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    _save_cart(request, cart)
    messages.info(request, f'"{product.name}" removido do carrinho.')
    return redirect("cart_detail")


@require_POST
def clear_cart(request):
    """
    Esvazia o carrinho.
    """
    _save_cart(request, {})
    messages.info(request, "Carrinho esvaziado.")
    return redirect("cart_detail")
