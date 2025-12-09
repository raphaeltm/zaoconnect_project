from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm, Registerform
from .models import Contact, Product


def index(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'index.html', {'products': products})

def cart(request):
    return render(request, 'cart.html')

def base(request):
    return render(request, 'base.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            Contact.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Thanks for reaching out. We will get back to you soon.')
            return redirect('contact')
        messages.error(request, 'All fields are required.')
    return render(request, 'contact.html')


def register(request):
    if request.method == 'POST':
        form = Registerform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = Registerform()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')


def logout_user(request):
    logout(request)
    return redirect('index')

@staff_member_required
def product_admin_list(request):
    products = Product.objects.all()
    return render(request, 'admin/products_list.html', {'products': products})


@staff_member_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_admin_list')
    else:
        form = ProductForm()
    return render(request, 'admin/product_form.html', {'form': form, 'action': 'Add'})


@staff_member_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_admin_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_form.html', {'form': form, 'action': 'Edit', 'product': product})


@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_admin_list')
    return render(request, 'admin/product_confirm_delete.html', {'product': product})
