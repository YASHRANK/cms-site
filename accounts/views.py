from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import Customer, Product, Order, Tag # models - database tables 

from accounts.forms import OrderForm ,CustomerForm, CreateUserForm  ## model - forms

from django.contrib.auth.forms import UserCreationForm  # customixed form  - from [ auth.User ]
from django.contrib.auth import authenticate, login, logout # authentication functions 

from django.contrib.auth.decorators import login_required # django builtin decorator 
from .decorators import unauthenticated_user, allowd_users, admin_only  ##custom decoretor 
from django.contrib.auth.models import Group

from django.forms import inlineformset_factory # to generate formset from single form 

from .filters import OrderFilter # search filter 

from django.contrib import messages # messsage system 

#---------------registration 
@unauthenticated_user
def register(request):

    form = CreateUserForm()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # returns username 
            username = request.POST['username'] 
            
            group = Group.objects.get(name='customer') # query to get customer group 
            user.groups.add(group)                     # and add each new user to customer group 

            Customer.objects.create(
                user=user,
                name=username,
                email= request.POST['email']
            )

            messages.success(request, f'Account created for {username}')
            return redirect('login')

    context= {'form':form}
    return render(request , 'accounts/register.html', context)

#---------------login
@unauthenticated_user
def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is invalid !')

    context= {}
    return render(request , 'accounts/login.html', context)
    


#---------------logout
def logout_user(request):
    logout(request)
    return redirect('login')


#--------------- homepage - dashboard
@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'customers':customers, 'orders':orders,
               'total_orders':total_orders, 'delivered':delivered,'pending':pending}
    return render(request, 'accounts/dashboard.html', context)

#--------------- product list table
@login_required(login_url='login')
@admin_only
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})

#--------------- customer details 
@login_required(login_url='login')
@allowd_users(allowed_roles=['admin'])
def customers(request , pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    order_filter = OrderFilter(request.GET , queryset=orders )
    orders = order_filter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'order_filter':order_filter}
    return render(request, 'accounts/customers.html',context)

#--------------- create customer from dashboard
@login_required(login_url='login')
@allowd_users(allowed_roles=['admin'])
def create_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = { 'form': form}
    return render(request, 'accounts/create_customer.html', context)

#---------------create order from customer details page
@login_required(login_url='login')  
@allowd_users(allowed_roles=['admin']) 
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    #------- for single - single orders --------
    # form = OrderForm(initial={'customer':customer}) 

    #------- for bunch of orders --------
    create_order_formset = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    formset = create_order_formset(queryset=Order.objects.none() ,instance=customer)
    if request.method == "POST":
        formset = create_order_formset(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset, 'customer':customer}
    return render(request, 'accounts/create_order.html',context)

#------- update order from dashboard
@login_required(login_url='login')
@allowd_users(allowed_roles=['admin'])
def update_order(request, pk):
        
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/update_order.html',context)

#------- delete order from dashboard
@login_required(login_url='login')
@allowd_users(allowed_roles=['admin'])
def delete_order(request, pk):
    
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context={'order': order}
    return render(request, 'accounts/delete_order.html', context)

@login_required(login_url='login')
@allowd_users(allowed_roles=['customer'])
def user_page(request):
    
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context= {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowd_users(allowed_roles=['customer'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES , instance=customer)
        if form.is_valid():
            form.save()
            

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)