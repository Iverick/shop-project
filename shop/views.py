from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


# http://localhost:8000/
# or http://localhost:8000/<category_slug>/
def product_list(request, category_slug=None):
    '''
    Root page for the shop.
    View should display list of all available products,
    or available products of the specific category if <category_slug>
    provided.

    Args:
        category_slug(str): 'tea'
    '''
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


# http://localhost:8000/<id>/<slug>/
def product_detail(request, id, slug):
    '''
    View returns page contains detailed info about selected product

    Args:
        id(int): '1' (quite obvious, isn't it)
        slug(str): 'tea-powder'
    '''
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })
