from webbrowser import get
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm



def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    delivered = orders.filter( status='delivered').count()
    pending = orders.filter(status = 'pending').count()
    
    context = { 'customers' : customers , 'orders' : orders ,'total_orders' : total_orders, 'delivered' : delivered , 'pending' : pending } # 

    return render( request, 'accounts/dashboard.html',context )
   

def products(request):

      products = Product.objects.all()

      return render( request, 'accounts/products.html',{ 'products' : products})


def customer(request,pk):
      #if request.method == "POST":
      #       search = request.POST['search']
      #      customer = Customer.objects.get(id=pk)
      #     customer = Job.objects.filter(detail__contains = s)


      customer = Customer.objects.get(id=pk)
      orders = customer.order_set.all()
      total_orders= customer.order_set.all().count
      context = { 'customer' : customer ,'orders' : orders ,'total_orders' : total_orders }

      return render( request, 'accounts/customer.html',context)


def create_customer(request):
      if request.method == 'GET':
            context = { }  
            return render( request, 'accounts/create_customer.html',context )
      else:
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            customer = Customer(name= name,email = email,phone = phone)
            customer.save()
            context = {"name":name ,"email":email}  
            return redirect(home)
 

def update_customer(request,pk):
      if request.method == 'GET':
            customer = Customer.objects.get(id=pk)
            context = {"customer":customer }  
            return render( request, 'accounts/update_customer.html',context )
      else:
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            customer = Customer.objects.get(id=pk)
            customer.name = name
            customer.email = email
            customer.phone = phone
            customer.save()
            context = {"name":name ,"email":email}  
            return redirect(home)
 

def createOrder(request , pk):
      OrderFormSet = inlineformset_factory(Customer, Order , fields=('Product','status'))
      customer = Customer.objects.get(id=pk)
      formset = OrderFormSet(instance = customer)

      
      #form = OrderForm(initial={'Customer': customer})
      if request.method == 'POST':
            #form = OrderForm(request.POST)
            formset = OrderFormSet(request. POST ,instance = customer)
            if formset.is_valid():
                  formset.save()
                  return redirect("/")

      context = { 'formset':formset } 
      return render( request, 'accounts/order_form.html',context)


def updateOrder(request,pk):
      order = Order.objects.get(id = pk)
      form = OrderForm(instance=order)

      if request.method == 'POST':
                  form = OrderForm(request.POST,instance=order)
                  if form.is_valid():
                        form.save()
                        return redirect("/")


      
      context = { 'form':form } 
      return render( request, 'accounts/order_update.html',context)


def deleteOrder(request,pk):
      order = Order.objects.get(id = pk)
      if request.method == 'POST':
            order.delete()
            return redirect("/")
      

      
     
      context = { 'item':order } 
      
      return render( request, 'accounts/delete.html',context)
