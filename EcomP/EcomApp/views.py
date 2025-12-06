import random
from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
from .models import Product,CartItem,Order
from .forms import CreateUserForm,AddProduct
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import razorpay


# Create your views here.
def index(request):
    products= Product.objects.all()
    context = {}
    context['products']=products
    return render(request,"index.html",context)

def view(request,pid):
    products=Product.objects.get(product_id=pid)
    context = {'products':products}
    return render(request,"view.html",context)

def cart(request):
    
    if request.user.is_authenticated:
        allproducts = CartItem.objects.filter(user = request.user)
    else:
        return redirect("/login")
    context = {}
    context['cart_items'] = allproducts
    total_price = 0
    
    for x in allproducts:
        total_price +=(x.product.price * x.quantity)
        print(total_price)
        context['total'] = total_price
        length = len(allproducts)
        context['items'] = length
    return render(request,"cart.html",context)

def add_cart(request,pid):
    products=Product.objects.get(product_id=pid)
    user = request.user if request.user.is_authenticated else None
    print(products)
    if user:
        cart_item,created = CartItem.objects.get_or_create(product=products,user=user)
    else:
        return redirect("/login")
        #cart_item,created = CartItem.objects.get_or_create(product=products)
    print(cart_item,created)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect("/cart")


def range(request):
    if request.method == "GET":
        return redirect("/")
    else:
        r1 = request.POST.get["min"]
        r2 = request.POST.get["max"]
        print(r1,r2)
    if r1 is not None and r2 is not None and r1 != "" and r2 != "" :
        queryset = Product.objects.filter(price_range = (r1,r2))
        #queryset = Product.prod.get_price_range(r1,r2)
        context = {'products':queryset}
        return render(request,"index.html",context)
    else:
        queryset = Product.objects.all()
        context = {'products':queryset}
        return render(request,"index.html",context)

def watchList(request):
    queryset = Product.prod.watch_list()
    print(queryset)
    context = {'products':queryset}
    return render(request,"index.html",context)

def laptopList(request):
    queryset = Product.prod.laptop_list()
    print(queryset)
    context = {'products':queryset}
    return render(request,"index.html",context)

def mobileList(request):
    queryset = Product.prod.mobile_list()
    print(queryset)
    context = {'products':queryset}
    return render(request,"index.html",context)

def removeCart(request,pid):
    cart_item = CartItem.objects.filter(product_id=pid,user=request.user)
    cart_item.delete()
    return redirect("/cart")


def search(request):
    query = request.POST['q']
    
    print(f"Recevied Quary is {query}")
    if not query:
        result = Product.objects.all()
    else:
        result = Product.objects.filter(
            Q(product_name__icontains = query)|
            Q(price__icontains = query)
        )
        
        return render(request,"index.html",{'results':result,'query':query})

# Low to High
def sort(request):
    queryset = Product.objects.all().order_by("price")
    context = {'products':queryset}
    return render(request,"index.html",context)

def sorth(request):
    queryset = Product.objects.all().order_by("-price")
    context = {'products':queryset}
    return render(request,"index.html",context)

# Update the product Quantity in Cart
def updatqty(request,uval,pid):
    #products = Product.objects.get(product_id = pid)
    user = request.user
    c = CartItem.objects.filter(product_id = pid, user=user)
    print(c)
    print(c[0])
    print(c[0].quantity)
    if uval == 1:
        a = c[0].quantity+1
        c.update(quantity = a)
        print(c[0].quantity)
    else:
        a = c[0].quantity-1
        c.update(quantity = a)
        print(c[0].quantity)

    return redirect("/cart")

def register_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,("User Created Successfully"))
            return redirect("/login")
        else:
            messages.error(request,"Incorrect Password Format")
    context = {'form':form}
    return render(request,"register.html",context)

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been logged in !!"))
            return redirect("/")
        else:
            messages.error(request,"Incorrect username or password")
            return redirect(request,"/login")
    else:
        return render(request,"login.html")
    


def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out in !!")
    return redirect("/")

def viewOrder(request):
    c = CartItem.objects.filter(user = request.user) #1
    """ oid = random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id = oid, product_id = x.product.product_id, user = request.user, quantity = x.quantity) #2
    orders = Order.objects.filter(user = request.user, is_completed = False) """
    context = {}
    context['cart_items'] = c
    total_price = 0
    
    for x in c:
        total_price +=(x.product.price * x.quantity)
        print(total_price)
    context['total'] = total_price
    length = len(c)
    context['items'] = length
    
    return render(request,"viewOrder.html",context)

def makePayment(request):
    c = CartItem.objects.filter(user = request.user)
    oid = random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id = oid, product_id = x.product.product_id, user = request.user, quantity = x.quantity) #2
    orders = Order.objects.filter(user = request.user, is_completed = False)
    orders = Order.objects.filter(user = request.user, is_completed = False)
    total_price = 0
    
    for x in orders:
        total_price +=(x.product.price * x.quantity)
        oid = x.order_id
        print(oid)
    client = razorpay.Client(auth=("rzp_test_pFkJjUvRgGGsSd", "QGBA6cx65vBEF7H470b8dUEF"))
    data = {
    "amount": total_price * 100,
    "currency": "INR",
    "receipt": "oid"}
    payment = client.order.create(data = data)
    context = {}
    context['data'] = payment
    context['amount'] = payment["amount"]
    #emptying cart
    
    c.delete()
    # Order completed = True
    orders.update(is_completed = True)
    return render(request,"payment.html",payment)

def inserProduct(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "GET":
            form = AddProduct()
            return render(request,"insertProd.html",{'form':form})
        else:
            form = AddProduct(request.POST,request.FILES or None)
      
            if form.is_valid():
                form.save()
                messages.success(request,("Product Entered Successfully"))
                return redirect("/")
            else:
                messages.error(request,"Incorrect data")
                return render(request,"insertProd.html",{'form':form})
    else:
        return redirect("/login")