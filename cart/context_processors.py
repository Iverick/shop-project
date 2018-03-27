'''
Adds cart object to the project context_processors
'''
from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}
