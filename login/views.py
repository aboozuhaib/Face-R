from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create your views here.

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('/dashboard')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    

    else:
        return render(request, 'login.html' ,{'title':"login"})