from django.shortcuts import render,redirect
from django.contrib import messages
# from django.contrib.auth import login,authenticate,logout
from django.contrib.auth import authenticate,login,logout

from .models import *
import requests
import json

# Create your views here.

def get_Books_data():
    api_url = f"https://frappe.io/api/method/frappe-library?page=2&title=and"
    response = requests.get(api_url)
    data = response.json()
  
    return data

    # api_url =  f"https://frappe.io/api/method/frappe-library?page=2&title=and"
    # response = requests.get(api_url)
    # data = response.json()
    # text = json.dumps(data, sort_keys=True, indent=4)
    # return text

   


def book_view(request):
    api_url = f"https://frappe.io/api/method/frappe-library?page=2&title=and"
    response = requests.get(api_url)
    data = response.json()
    context = {'book_data':data}   
    # for i,item in context.items():
    #     print(i)
    #     for a in item:
    #         print(item[a][0])
    return render(request, 'home.html', context)


def register(request):
    if(request.method == 'POST'):
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        
        userAuth = User.objects.filter(username = username)
        if(userAuth.exists()):
            messages.info(request, 'Username Alraday exists!')
            return redirect('/register')

        queryset = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        queryset.set_password(password)
        queryset.save()
        messages.info(request, 'Account Create Successfully!')
        return redirect('/register')
    return render(request, 'register.html')



def login_user(request):
    if(request.method == 'POST'):
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        # if username doesn't exists then message to the user.
        user = User.objects.filter(username = username)
        if(not user.exists()):
            messages.error(request, 'Username Does not exists!')
            return redirect('/login_user')
        #cheak  account ahea ka nahi
        userAuth = authenticate(username = username , password = password)
        if(userAuth is None):
            messages.error(request, 'Account does not exists')
            return redirect('/login_user')
        else:
            #acccout assel ther value fit houn user login hoil
            login(request, userAuth)
            return redirect('/')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/login_user')
    
