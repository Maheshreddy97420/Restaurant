from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            if user.is_staff:
                return redirect('admin_home')
            else:
                return redirect('user_home')
        else:
            return render(request,'login_.html',{'error':'Invalid username or password'})
    return render(request,'login_.html')

def logout_(request):
    logout(request)
    return redirect('login_')
