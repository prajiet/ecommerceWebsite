from django.http import HttpResponse
from django.http import Http404
from django.apps import AppConfig

from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from .forms import UserForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Category
from .models import Products
from .models import Cart,ProductOrder
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import operator
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

def index ( request ):
        all_category=Category.objects.all()
        p=Products.objects.all()
        query=request.GET.get("q")
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(product_name=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(content_brand=q) for q in query_list))
            )
        context={'all_category' : all_category,'user':request.user,'p':p,}
        return render(request, 'products/index.html', context)



def detail(request , category_id):
    category=get_object_or_404(Category,pk=category_id)

    c=Category.objects.all()
    product=Products.objects.select_related().filter(product_category = category_id)
    paginator=Paginator(product,6)
    page=request.GET.get('page')
    try:
        product=paginator.page(page)
    except PageNotAnInteger:
        product=paginator.page(1)
    except EmptyPage:
        product=paginator.page(paginator.num_pages)

    return render(request, 'products/detail.html', {'category': category, 'product':product,'c':c,'user':request.user,})



def product_detail(request,category_id ,product_id):
    c=get_object_or_404(Category,pk= category_id)
    all_category=Category.objects.all()
    p=get_object_or_404(Products,pk=product_id)
    products=Products.objects.all()
    page_title=p.product_name
    meta_description=p.product_description
    if request.method =='POST':
        postdata=request.POST.copy()
        form=ProductAddToCartForm(request,postdata)
        if form.is_valid():
            cart.add_to_cart(request)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
        else:
            form=ProductAddToCartForm(request=request, label_suffix=':')
        form.fields['product_id'].widget.attrs['value']=product_id
        request.session.set_test_cookie()
    return render(request , 'products/product_detail.html',{'p':p,'all_category':all_category,'user':request.user,'c':c,'products':products})

def search(request):
    query = request.GET.get("q")
    p=Products.objects.filter(product_name=query)

    return render(request,'products/search.html',{'p':p})


class UserFormView(View):
    form_class=UserForm
    template_name='products/registration_form.html'
    all_category=Category.objects.all()
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user=authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('products:index')


        return render(request,self.template_name,{'form':form,'all_category':all_category,'user':request.user})

def add_to_cart(request,product_id):
    if request.user.is_authenticated():
        try:
            product=Products.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            pass
        else:
            try:
                cart=Cart.objects.get(user=request.user,active=True)
            except ObjectDoesNotExist:
                cart=Cart.objects.create(user=request.user)
        cart.add_to_cart(product_id)
        return redirect('products:cart')
    else:
        return redirect('products:index')

def remove_from_cart(request,product_id):
    if request.user.is_authenticated():
        try:
            product=Products.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            pass
        else:
            cart=Cart.objects.get(user=request.user,active=True)
            cart.remove_from_cart(product_id)
        return redirect('products:cart')
    else:
        return redirect('products:index')

def cart(request):
    if request.user.is_authenticated():
        cart=Cart.objects.filter(user=request.user.id,active=True)
        orders = ProductOrder.objects.filter(cart=cart)
        total=0
        count=0
        for order in orders:
            total += (order.product.product_price *order.quantity)
            count += order.quantity
        context = {'cart':cart,'total':total,'count':count,'orders':orders}
        return render(request , 'products/cart.html', context)
    else:
        return redirect('products:index')
















