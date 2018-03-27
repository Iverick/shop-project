# django imports
from django.conf.urls import url
# local imports
from . import views

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
]
