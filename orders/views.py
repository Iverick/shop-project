# django imports
from django.shortcuts import render
# local imports
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
# custom cart app imports
from cart.cart import Cart


# http://localhost:8000/orders/create/
def order_create(request):
    '''
    Creates order with the given cart object from the request. Validates given
    data using OrderItem form. 
    If order saved and validated it launches asynchronous task using code from
    local tasks.py file.
    '''
    cart = Cart(request)

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(
                request,
                'orders/order/created.html',
                {'order': order}
            )
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )
