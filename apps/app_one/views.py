from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import logout


def admin(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    if user.user_level != 7:
        return redirect('/')
    else:
        context = {
            'users': User.objects.all(),
            'reviews': Review.objects.all(),
            'user': User.objects.get(id=request.session['user_id'])
        }
    return render(request, 'app_one/admin.html', context)

def log(request):
    return render(request, 'app_one/log.html')

def signup(request):
    return render(request, 'app_one/register.html')

def register(request):
    if request.method != "POST":
        return redirect('/logreg')
    result = User.objects.reg_validator(request.POST)
    if 'success' in result:
        request.session['user_id'] = result['success'].id
        return redirect('/')
    else:
        for key, value in result.items():
            messages.error(request, value)
        return redirect('/signup')

def login(request):
    if request.method != "POST":
        return redirect('/logreg')
    result = User.objects.log_validator(request.POST)
    if 'success' in result:
        request.session['user_id'] = result['success'].id
        return redirect('/')
    else:
        messages.error(request, "Check your Login or Password")
        return redirect('/log')


def logoff(request):
    logout(request)
    return redirect('/')

def deleteuser(request, u_id):
    user = User.objects.get(id=u_id)
    user.delete()
    return redirect('/admin')


def home(request):
    if not 'user_id' in request.session:
        context = {
            'allreviews': Review.objects.all()
        }      
    else:
        context = {
            'allreviews': Review.objects.all(),
            'user': User.objects.get(id=request.session['user_id'])
        }
    return render(request, 'app_one/home.html', context)

def dashboard(request, u_id):
    if not 'user_id' in request.session:
        context = {
            'their_reviews': Review.objects.filter(author=u_id)
        } 
    else:     
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'users': User.objects.get(id=u_id),
            'their_reviews': Review.objects.filter(author=u_id)
    }
  
    return render(request, 'app_one/dashboard.html', context)


def review(request):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        context={    
            'user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'app_one/review.html', context)


def reviewcreate(request):
    if request.method != "POST":
        return redirect('/review')
    else:
        user = User.objects.get(id=request.session['user_id'])
        Review.objects.create(
            title = request.POST['title'], 
            text = request.POST['text'], 
            rating = request.POST["rating"], 
            picture = request.FILES['picture'], 
            author = user)
    return redirect('/')


def update(request, r_id):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'review': Review.objects.get(id=r_id)
    }
    return render(request, 'app_one/editreview.html', context)


def reviewedit(request, r_id):
     if request.method == "POST":
        print(request.POST)
        errors = {}
     if len(request.POST['text']) == 0:
           errors['text'] = 'Text must present'
     if len(errors):
        for key,value in errors.items():
            messages.error(request, value)
        return redirect('/update/{}'.format(r_id))
     else:
        review = Review.objects.get(id=r_id)
        review.text = request.POST['text']
        review.save()
     context = {
        'reviews': Review.objects.get(id=r_id)
     }
     return redirect('/', context)

def deletereview(request, r_id):
    User.objects.get(id=request.session['user_id']),
    asplode = Review.objects.get(id=r_id)
    asplode.delete()
    return redirect('/')


def showreview(request, r_id):
    if not 'user_id' in request.session:
        context = {
            'review': Review.objects.get(id=r_id),
        }      
    else: 
        context = {
        'review': Review.objects.get(id=r_id),
        'user': User.objects.get(id=request.session['user_id']),  
    }
    return render(request, 'app_one/showreview.html', context)

def create_comment(request, r_id):
    if request.method != "POST":
        return redirect('/showreview')
    else:
         user = User.objects.get(id=request.session['user_id'])
         review = Review.objects.get(id=r_id)
         Comment.objects.create(
             text = request.POST['text'],
             comment_by = user,
             review_commented = review
         )
    return redirect('/')
