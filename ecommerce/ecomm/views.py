from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from ecomm.forms import UserForm,UserForm2,Update1,Update2,CheckoutForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserData,Productdata,Order,Category,UserOrder

# Create your views here.

def index(request):
    return render(request,"index.html")

def registration(request):
    registered = False

    if request.method == "POST":
        form = UserForm(request.POST)
        profile = UserForm2(request.POST, request.FILES)

        if form.is_valid() and profile.is_valid() :
            user = form.save()
            user.set_password(user.password)
            user.save()
            prof = profile.save(commit=False)
            prof.user = user 
            prof.save()
            messages.success(request,"Registered Successfully")
            return redirect('login')
        else:
            messages.error(request,"NOT Registered please try again!")
            return redirect('registration')
    else:
        form = UserForm()
        profile = UserForm2()

    return render(request, "registration.html", {"form": form, "profile": profile, "registered" :registered})
        
def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")


        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                messages.success(request,"Login successful")
                return redirect('home')

            else:
                messages.error(request,"user is not active")
        else:
            messages.error(request,"user credentials are invalid")


    return render(request,"login.html",{})

def home(request):
    product = Productdata.objects.all()
    categories = Category.objects.all()

    
    if request.method == "POST":
        if request.user.is_authenticated:  # Check if the user is authenticated
            selected_categories = request.POST.getlist('category')  # Use getlist to get multiple selected values

            if selected_categories:
                product = Productdata.objects.filter(category__category__in=selected_categories)
        else:
            # Redirect the user to the login page if they're not logged in
            return redirect('login')  # Assuming your login URL name is 'login'

    return render(request, "home.html", {"product": product, "categories": categories})


def user_logout(request):
    logout(request)

    return redirect('home')


def user_update(request):
    userprofile = UserData.objects.get(user= request.user)

    if request.method == "POST":
        user1 = Update1(request.POST, instance=request.user)
        user2 = Update2(request.POST,request.FILES, instance=userprofile)

        if user1.is_valid() and user2.is_valid():
            user1.save()
            user2.save()
            return redirect('profile')
    else:
        user1 = Update1(instance=request.user)
        user2 = Update2(instance=userprofile)
    return render(request,"update.html",{"user1":user1,"user2":user2})

def profile(request):

    userprofile = UserData.objects.get(user= request.user)

    return render(request,"profile.html",{"userprofile":userprofile})

def view_cart(request):

    cart = Order.objects.filter(user=request.user)
    

    price = (i.product.price * i.quantity for i in cart)

    total_price  =  sum(i.product.price * i.quantity for i in cart)


    return render(request,"cart.html",{"cart":cart,"total_price":total_price,"price":price})


def add_to_cart(request,id):
    product = Productdata.objects.get(id=id)
    price = product.price
    cart_item, created = Order.objects.get_or_create(product=product, user=request.user, price=price)
    if created:
        cart_item = cart_item # Unpack the tuple to get the CartItem object
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def update_cart(request):
    if request.method == 'POST':
        item_id_with_operation = request.POST.get('item_id')
        item_id, operation = item_id_with_operation.split('_')
        item_id = int(item_id)
        
        # Find the item in the cart
        item = Order.objects.get(id=item_id)

        # Update quantity
        if operation == 'increment':
            item.quantity += 1
        elif operation == 'decrement' and item.quantity > 1:
            item.quantity -= 1
        
        # Save the changes
        item.save()

    return redirect('cart')


def thankyou(request):

    

    user_orders = Order.objects.filter(user=request.user, status=True,)
    cart = Order.objects.filter(user=request.user)
    total_price = sum(order.quantity * order.price for order in user_orders)



    # Pass orders to the template for rendering
    return render(request, 'thankyou.html', {'user_orders': user_orders,"total_price":total_price})

def placedorder(request):

    try:
        user_orders = Order.objects.filter(user=request.user, status=True).order_by("-date")
        total_price = sum(order.quantity * order.price for order in user_orders)
        created_user_orders = []
        for order in user_orders:
            user_order = UserOrder.objects.create(
            user=order.user,
            product=order.product,
            quantity=order.quantity,
            price=order.price,
            address=order.address,
            phone=order.phone,
            status=order.status
            )
            
            created_user_orders.append(user_order)
            # Clear the user's cart after saving orders
        user_orders.delete()


    except Order.DoesNotExist:
        created_user_orders = []
        total_price = 0

    orders = UserOrder.objects.filter(user=request.user, status=True).order_by('-date')

    return render(request, 'placedorder.html', {'created_user_orders': created_user_orders, 'total_price': total_price, "orders":orders})
    # Pass orders to the template for rendering



def checkout(request):
    user_orders = Order.objects.filter(user=request.user, status=False)  # Get orders in the cart for the current user

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            
            # Update each order with the delivery address and phone number
            for order in user_orders:
                order.address = address
                order.phone = phone
                order.status = True  # Update order status to indicate it's been placed
                order.save()
            return redirect('thankyou')

            # Redirect to the thank you page
                
    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {"user_orders": user_orders, "form": form})


def remove_from_cart(request,id):

    order = get_object_or_404(Order, id=id)

    order.delete()

    return redirect('cart')

def reset(request):
    return render(request,"reset.html")


def search(request):

    product =  Productdata.objects.all()

    searched = request.POST.get('searched',"")

    data = []

    if searched:
        data = Productdata.objects.filter(name__icontains=searched)

    return render(request,"search.html",{"product":product,"searched":searched,"data":data})