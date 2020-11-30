from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    print(request.POST)
    return render(request, 'index.html')

def dashboard(request):
    print(request.POST)
    if 'uid' not in request.session:
        return redirect('/')
    else:
        logged_in_user = User.objects.get(id = request.session['uid'])
        context = {
            'shoes' : Shoe.objects.all(),
            'user' : logged_in_user
        }
        return render(request, 'dashboard.html', context)

def upload(request):
    print(request.POST)
    errors = Shoe.objects.shoe_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else: 
        logged_in_user = User.objects.get(id = request.session['uid'])
        this_shoe = Shoe.objects.create(
            brand = request.POST['brand'],
            name = request.POST['name'],
            size = request.POST['size'],
            desc = request.POST['desc'],
            uploaded_by = logged_in_user
        )
        print(this_shoe)
        return redirect('/dashboard')

def like(request, shoe_id):
    print(request.POST)
    this_shoe = Shoe.objects.get(id = shoe_id)
    this_shoe.liked = True
    this_shoe.save()
    return redirect('/dashboard')

def delete(request, shoe_id):
    print(request.POST)
    del_shoe = Shoe.objects.get(id = shoe_id)
    del_shoe.delete()
    return redirect('/dashboard')

def cop(request):
    print(request.POST)
    context = {
        'shoes' : Shoe.objects.filter(for_sale = True)
    }
    return render(request, 'cop.html', context)

def flip(request):
    print(request.POST)
    return render(request, 'flip.html')

def sell(request):
    print(request.POST)
    errors = Shoe.objects.sell_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/flip')
    else:
        sell_shoe = Shoe.objects.create(
            brand = request.POST['brand'],
            name = request.POST['name'],
            size = request.POST['size'],
            desc = request.POST['desc']
        )
        sell_shoe.for_sale = True
        sell_shoe.save()
        print('making listing')
        return redirect('cop')

def discuss(request):
    print(request.POST)
    return render(request, 'discuss.html')

def shoebox(request):
    print(request.POST)
    return render(request, 'shoebox.html')
    
def myshoebox(request):
    print(request.POST)
    return redirect('/dashboard')

def register(request):
    print(request.POST)
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hashed_pw)
        created_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
        )
        request.session['uid'] = created_user.id
    return redirect('/dashboard')

def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(email = request.POST['confirm_email'])
        request.session['uid'] = user[0].id
        return redirect('/dashboard')

def logout(request):
    print(request.POST)
    request.session.flush()
    return redirect('/')