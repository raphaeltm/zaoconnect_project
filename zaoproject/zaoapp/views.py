from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse

from .forms import ProductForm, Registerform, UserProfileForm, CustomPasswordChangeForm
from .models import Contact, Product, Cart, CartItem
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime
import json


@staff_member_required
def product_admin_report_pdf(request):
    """Generate a simple PDF report of products for staff users.

    This uses ReportLab; if ReportLab is not installed the view returns
    an error response asking to install it (pip install reportlab).
    """
    try:
        from reportlab.lib.pagesizes import A4  # type: ignore
        from reportlab.pdfgen import canvas # type: ignore
    except Exception:
        return HttpResponse(
            "Report generation requires ReportLab. Install with: pip install reportlab",
            status=500,
            content_type='text/plain'
        )

    buffer = BytesIO()
    page_size = A4
    c = canvas.Canvas(buffer, pagesize=page_size)
    width, height = page_size

    # Header
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height - 50, 'Products Report')
    c.setFont('Helvetica', 10)
    c.drawString(40, height - 70, f'Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}')

    # Table header
    y = height - 100
    c.setFont('Helvetica-Bold', 11)
    c.drawString(40, y, 'Name')
    c.drawString(300, y, 'Price')
    c.drawString(380, y, 'Stock')
    c.drawString(450, y, 'Active')
    y -= 18
    c.setFont('Helvetica', 10)

    products = Product.objects.all().order_by('name')
    line_height = 14
    for p in products:
        if y < 60:  # start new page
            c.showPage()
            y = height - 50
        name = (p.name[:50] + '...') if len(p.name) > 53 else p.name
        c.drawString(40, y, name)
        c.drawString(300, y, f'{p.price}')
        c.drawString(380, y, f'{p.stock}')
        c.drawString(450, y, 'Yes' if p.is_active else 'No')
        y -= line_height

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()

    resp = HttpResponse(pdf, content_type='application/pdf')
    resp['Content-Disposition'] = 'attachment; filename="products_report.pdf"'
    return resp


def index(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'index.html', {'products': products})

def cart(request):
    return render(request, 'cart.html')

def order(request):
    return render(request, 'order.html')

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
            return redirect('index')
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
    """User profile page with edit form and password change."""
    user = request.user
    profile_form = None
    password_form = None
    profile_updated = False
    password_updated = False
    
    # Handle profile form submission
    if request.method == 'POST' and 'update_profile' in request.POST:
        profile_form = UserProfileForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            # Store phone number in user's first_name as a workaround (no phone field on User)
            # Alternatively, extend User with a UserProfile model if needed
            messages.success(request, 'Profile updated successfully.')
            profile_updated = True
            return redirect('profile')
        password_form = CustomPasswordChangeForm(user)
    # Handle password change form submission
    elif request.method == 'POST' and 'change_password' in request.POST:
        password_form = CustomPasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, 'Password changed successfully.')
            password_updated = True
            return redirect('profile')
        profile_form = UserProfileForm(instance=user)
    else:
        profile_form = UserProfileForm(instance=user)
        password_form = CustomPasswordChangeForm(user)
    
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'profile.html', context)


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


@login_required
def get_cart(request):
    """Get the current user's cart as JSON."""
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    
    items = []
    for item in cart.items.all():
        items.append({
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'image_url': item.product.image.url if item.product.image else None,
        })
    
    return JsonResponse({
        'items': items,
        'total': float(cart.get_total()),
    })


@login_required
def update_cart(request):
    """Add or update an item in the user's cart."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id or quantity < 1:
            return JsonResponse({'error': 'Invalid product_id or quantity'}, status=400)
        
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        if quantity == 0:
            # Remove item
            CartItem.objects.filter(cart=cart, product=product).delete()
        else:
            # Add or update item
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product,
                defaults={'quantity': quantity}
            )
            if not item_created:
                cart_item.quantity = quantity
                cart_item.save()
        
        return JsonResponse({
            'success': True,
            'total': float(cart.get_total()),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def clear_cart(request):
    """Clear all items from the user's cart."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()
    
    return JsonResponse({'success': True})


def find_product_by_name(request):
    """Find a product by name (exact or partial match) and return id/price.

    This is used as a fallback when a product tile on the page doesn't include
    a `data-product-id` attribute (static placeholders). The client may call
    this with ?name=... and receive a JSON response with product details.
    """
    name = request.GET.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'name parameter required'}, status=400)

    # Try exact case-insensitive match first, then a contains match
    product = Product.objects.filter(name__iexact=name).first()
    if not product:
        product = Product.objects.filter(name__icontains=name).first()

    if not product:
        return JsonResponse({'error': 'product not found'}, status=404)

    return JsonResponse({'id': product.id, 'name': product.name, 'price': float(product.price)})
