from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Users
import bcrypt
import math
# from datetime import 
from datetime import datetime, date


# Create your views here.
def index(request):
   ## MAYBE ADD SOME AJAX if there is time
    return render(request, 'index.html')

def success(request):
    pages = []
    users = Users.objects.all()
    print('i total = ', math.ceil(users.count()/5))
    for i in range(1,math.ceil(users.count()/5)):
        print("i = ", i)
        pages.append(i+1)
        print(pages)
        # request.session['list']=users
    context={
        'users': users[:5],
        'pages': pages,
    }
    return render(request, 'data.html', context)

def register(request):
    request.session.flush()
    if request.method == 'POST':
        errors = Users.objects.userValidator(request.POST)
        unique = Users.objects.filter(email=request.POST['email'])
         
        if len(unique)>0:
            errors['duplicate'] = "This email was already used to create an account."
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request, value) 
            return redirect ('/')
        else: 
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            Users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['reg_or_log']="Registration"
            newuser = Users.objects.get(email=request.POST['email'])
            request.session['user_id'] = newuser.id
            request.session['name'] = newuser.first_name
                        
            return redirect('/success')
    else:
        return redirect ('/')

def check_login(request):
    request.session.flush()
    this_user = Users.objects.filter(email=request.POST['email'])
    errors = {}
    if this_user:
        this_user=this_user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
            request.session['user_id']=this_user.id
            request.session['name'] = f"{this_user.first_name} {this_user.last_name}"
            request.session['reg_or_log']="Login"
            return redirect('/success')
        else:
            errors['pass'] = 'Incorrect Password'
    else:
        errors['user'] = 'Invalid Email Address'
    if len(errors)>0:
        request.session['errors'] = errors  
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')
        
def user_details(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context={
        'user' : Users.objects.get(id=user_id),
        'logged_user': Users.objects.get(id=request.session['user_id']),
    }
    return render(request, 'user.html', context)

def user_edit(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.session['user_id'] == user_id:
        context = {
            'user' : Users.objects.get(id=user_id)
        }
        return render(request, 'edit_account.html', context)
    else: 
        return redirect('/success')
    
def update(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    request.session['update'] = ''
    if request.method == "POST":
        logged_user = Users.objects.get(id=user_id)
        errors = Users.objects.userUpdateValidator(request.POST)
        if not logged_user.email == request.POST['email']:
            if Users.objects.filter(email=request.POST['email']):
                errors['duplicate']="There is already an account with this Email Address"
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect (f'/user/{user_id}/edit')
        
        logged_user.first_name = request.POST['first_name']
        logged_user.last_name  = request.POST['last_name']
        logged_user.email = request.POST['email']
        logged_user.save()
        request.session['update'] = 'Successful Updates!'
        return redirect (f'/user/{user_id}/edit') 
    else:
        return redirect (f'/user/{user_id}/edit')
    
def search(request):
    print('start search')   
    pages = []
    if request.method == "POST":
        first_name = request.POST['first_name']
        print("error")
        last_name = request.POST['last_name']
        from_date = request.POST['from_date']
        if not from_date:
            from_date = date(1900,1,1)
        
            
        to_date = request.POST['to_date']
        print('to_date', to_date)
        if not to_date:
            to_date = date.today()
     
            
        request.session['first_name'] =first_name
        request.session['last_name'] = last_name
        request.session['from_date'] = str(from_date)
        request.session['to_date'] = str(to_date)
        
        print("request.session to_date as str: ", str(to_date))
        print("request.session from_date as str: ", str(from_date))
        
        users = Users.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name, created_at__date__range=(from_date, to_date))
        print(users)
        for i in range(1,math.ceil(users.count()/5)):
            pages.append(i+1)
        print('pages: ', pages)
        context = {
            'users': users[:5],
            'pages': pages,
        }
      
        print('filter complete')
    print('gonna try to render AJAX')
    return render(request, 'snippet.html', context)    

def page(request, page_no):
    print('page no is: ', page_no)
    pages=[]
    if 'first_name' not in request.session:
        users = Users.objects.all()
    else: 
        first_name = request.session['first_name']
        last_name = request.session['last_name']
        from_date = datetime.strptime(request.session['from_date'], '%Y-%m-%d')
        to_date = datetime.strptime(request.session['to_date'], '%Y-%m-%d')
        users = Users.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name, created_at__date__range=(from_date, to_date))
    
    for i in range(1,math.ceil(users.count()/5)):
        pages.append(i+1)
    context={
        'users': users[((5*page_no)-5):5*page_no],
        'pages': pages,
    }
    return render(request, 'snippet.html', context)


