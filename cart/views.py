from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# http://localhost:8000/cart/add/<product_id>/
@require_POST
def cart_add(request, product_id):
    '''
    View used to add product to the cart.
    Retrieves product object with the given product_id and validates it using
    CartAddProductForm. If form is valid then it adds products to the cart
    using add method of the cart object specified in cart.py module.
    Redirects to the main cart page after removing is done.
    Requires to be submited via POST request.

    Args:
        product_id(int): '1'
    '''
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )
    return redirect('cart:cart_detail')


# http://localhost:8000/cart/remove/<product_id>/
def cart_remove(request, product_id):
    '''
    View used to remove product from the cart.
    Selects product with the given product_id in the cart if it's added and
    removes it using remove method of the cart object specified in cart.py
    module.
    Redirects to the main cart page after removing is done.

    Args:
        product_id(int): '1'
    '''
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


# http://localhost:8000/cart/
def cart_detail(request):
    '''
    Returns cart objects stored is session.
    Displays list of products added to the cart and allows to change quantity
    of the product for every product element added using CartAddProductForm.

    View adds a Cart object to the main page of the shop when it's loaded.
    '''
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                       initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
