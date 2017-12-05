"""ecommercewebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.views import login,logout
from django.apps import AppConfig

app_name='products'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', login , {'template_name':'products/login.html'}),
    url(r'^logout/$', logout, {'template_name': 'products/logout.html'}),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^(?P<category_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^add/(?P<product_id>[0-9]+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove/(?P<product_id>[0-9]+)/$', views.remove_from_cart, name='remove_from_cart'),

    url(r'^(?P<category_id>[0-9]+)/(?P<product_id>[0-9]+)/$', views.product_detail, name='product_detail'),
    ]
