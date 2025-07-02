from django.shortcuts import render,redirect
from .models import Product
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from.forms import signupForm
# Create your views here.


def home(request):
    Products = Product.objects.all()
    return render(request,"store/home.html",{'Products':Products})

def about(request):
    return render(request,"store/about.html")



def product(request,pk):
    product = Product.objects.get(id = pk)
    return render(request,"store/product.html",{'product':product})




def login_user(request):
    if not request.user.is_authenticated:
        if request.method =="POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username = username,password = password)
            if user is not None:
                login(request,user)
                messages.success(request,"You have been logged in")
                return redirect('home')
            else:
                messages.success(request,("Invalid username or password"))
                return redirect("login")
        else:
            return render(request,"store/login.html")    
    else:
        return redirect("home")



def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out....thankyou for standing by..."))
    return redirect("home")




def register(request):
    if request.method =="POST":
        form = signupForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request,"You have been registered...")
            return redirect("home")
        else:
            messages.success(request,"error signing in..try again")
            return redirect('register')
        
    else:
        form = signupForm()
        return render(request,"store/register.html",{'form':form})
    

