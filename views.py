from itertools import count

from django.shortcuts import render, redirect
from .models import Category, Subcategory, Image, Cart, User,Wishlist,Address,Payment,Order
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import razorpay
from django.conf import settings
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def project(request):
    return render(request,'project.html')

def services(request):
    return render(request,'services.html')

def login(request):
    error = None

    if request.POST:
        e = request.POST['email']
        p = request.POST['password']

        user = User.objects.filter(email=e, password=p).first()

        if user:
            request.session['is_login'] = True
            request.session['userid'] = user.id
            return redirect('/')
        else:
            error = "Invalid email or password"

    return render(request, 'login.html', {'error': error})
def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')

def blogsingle(request):
    return render(request,'blogsingle.html')

def product(request):
    return render(request,'product.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        obj = User(
            username=username,
            email=email,
            password=password
        )
        obj.save()
        return redirect('/login')

    return render(request, 'signup.html')

def category(request):
    categories = Category.objects.all()
    images = Image.objects.select_related('c_id')

    category_data = []
    for cat in categories:
        img = images.filter(c_id=cat).first()
        category_data.append({
            'category': cat,
            'image': img
        })

    return render(request, 'category.html', {'category_data': category_data})

def subcategory(request, c_id):

    scategory = Subcategory.objects.filter(c_id=c_id)
    images = Image.objects.all()
    #  Get selected category
    category = Category.objects.get(c_id=c_id)

    subcategory_data = []

    for scat in scategory:
        img = images.filter(s_id=scat).first()

        subcategory_data.append({
            'subcategory': scat,
            'image': img,
            'price': scat.price,
            'detail': scat.detail,
            's_name': scat.s_name
        })

    return render(request, 'subcategory.html', {
        'subcategory_data': subcategory_data,
        'category': category  # send category to template
    })

def product_detail(request, id):
    product = Subcategory.objects.get(s_id=id)

    image = Image.objects.filter(s_id=product).first()

    return render(request, 'product_detail.html', {
        'product': product,
        'image': image
    })
def add_to_cart(request, id):

    if 'userid' not in request.session:
        return redirect('/login')

    product = Subcategory.objects.get(s_id=id)

    user = User.objects.get(id=request.session['userid'])

    Cart.objects.create(
        user_id=user,
        s_id=product,
        c_id=product.c_id,
        Qty=1
    )
    messages.success(request, "Product saved in cart successfully")
    return redirect('/view_cart')

def view_cart(request):

    if 'userid' not in request.session:
        return redirect('/login')

    user = User.objects.get(id=request.session['userid'])

    cart_items = Cart.objects.filter(user_id=user,is_ordered=False)

    grand_total = 0
    for item in cart_items:
        item.total_price = item.s_id.price * item.Qty
        grand_total += item.total_price
    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })

def remove_cart(request, id):

    if 'userid' not in request.session:
        return redirect('/login')

    cart_item = Cart.objects.get(cart_id=id)

    cart_item.delete()

    return redirect('/view_cart')

def increase_qty(request, id):
    cart_item = Cart.objects.get(cart_id=id)
    cart_item.Qty += 1
    cart_item.save()
    return redirect('/view_cart')


def decrease_qty(request, id):
    cart_item = Cart.objects.get(cart_id=id)

    if cart_item.Qty > 1:
        cart_item.Qty -= 1
        cart_item.save()

    return redirect('/view_cart')

def add_to_wishlist(request, id):

    if 'userid' not in request.session:
        return redirect('/login')

    user = User.objects.get(id=request.session['userid'])

    product = Subcategory.objects.get(s_id=id)

    already = Wishlist.objects.filter(user_id=user, s_id=product)

    if already.exists():
        return redirect('/wishlist')

    Wishlist.objects.create(
        user_id=user,
        s_id=product
    )

    return redirect('/wishlist')

def wishlist(request):

    if 'userid' not in request.session:
        return redirect('/login')

    user = User.objects.get(id=request.session['userid'])

    wishlist_items = Wishlist.objects.filter(user_id=user)

    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items
    })
def remove_wishlist(request, id):

    item = Wishlist.objects.get(w_id=id)

    item.delete()

    return redirect('/wishlist')


def checkout(request):

    user_id = request.session.get('userid')

    if not user_id:
        return redirect('/login')

    user = User.objects.get(id=user_id)
    cart_items = Cart.objects.filter(user_id=user, is_ordered=False)

    grand_total = 0
    for item in cart_items:
        item.total_price = item.s_id.price * item.Qty
        grand_total += item.total_price

    if request.method == "POST":

        # ✅ ADDRESS SAVE
        Address.objects.create(
            Name=request.POST.get('name'),
            Address=request.POST.get('address'),
            Pincode=request.POST.get('pincode'),
            state=request.POST.get('state'),
            Contact=request.POST.get('contact'),
            Comments=request.POST.get('comments'),
            user_id=user
        )

        # ✅ ORDER SAVE
        order = Order.objects.create(
            Total=grand_total,
            user_id=user
        )

        # ✅ LINK CART ITEMS WITH ORDER (IMPORTANT 🔥)
        for item in cart_items:
            item.is_ordered = True
            item.o_id = order.o_id
            item.save()

        # GET PAYMENT ID
        payment_id = request.POST.get('razorpay_payment_id')

        # ✅ PAYMENT STATUS
        status = "Complete" if payment_id else "Pending"

        # ✅ SAVE PAYMENT
        Payment.objects.create(
            o_id=order.o_id,
            Total=grand_total,
            Date=timezone.now().date(),
            Time=timezone.now().time(),
            Status=status,
            Type="Online",
            user_id=user.id
        )

        return redirect('/view_cart')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })


def create_razorpay_order(request):

    user_id = request.session.get('userid')
    user = User.objects.get(id=user_id)

    cart_items = Cart.objects.filter(user_id=user)

    total = 0
    for item in cart_items:
        total += item.s_id.price * item.Qty

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": int(total * 100),
        "currency": "INR"
    })

    return JsonResponse({
        "order_id": order['id'],
        "amount": order['amount'],
        "key": settings.RAZORPAY_KEY_ID
    })


def search_products(request):
    query = request.GET.get('q')

    results = Subcategory.objects.none()

    if query:
        results = Subcategory.objects.filter(
            Q(s_name__icontains=query) |
            Q(detail__icontains=query)
        ).prefetch_related('image_set')

    return render(request, 'search_results.html', {
        'query': query,
        'results': results
    })

def your_order(request):

    user_id = request.session.get('userid')

    if not user_id:
        return redirect('/login')

    user = User.objects.get(id=user_id)

    orders = Order.objects.filter(user_id=user).order_by('-o_id')

    order_data = []

    for order in orders:

        payment = Payment.objects.filter(o_id=order.o_id).first()
        address = Address.objects.filter(user_id=user).order_by('-a_id').first()

        products = Cart.objects.filter(o_id=order.o_id, is_ordered=True)

        product_list = []

        for item in products:
            # 🔥 GET IMAGE FROM Image TABLE
            image = Image.objects.filter(s_id=item.s_id).first()

            product_list.append({
                'name': item.s_id.s_name,
                'price': item.s_id.price,
                'qty': item.Qty,
                'image': image.image.url if image else None
            })

        order_data.append({
            'order': order,
            'payment': payment,
            'address': address,
            'products': product_list
        })

    return render(request, 'your_order.html', {
        'order_data': order_data
    })

