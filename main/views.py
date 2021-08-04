from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def login(request):
    user = User.objects.filter(email=request.POST["email"])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(), logged_user.password.encode()
        ):
            request.session["log_user_id"] = logged_user.id
            return redirect("/home")
    messages.error(request, "Invalid email or password")
    return redirect("/")


def create_user(request):
    errors = User.objects.user_validator(request.POST)

    user = User.objects.filter(email=request.POST["email"])

    if user:
        messages.error(request, "Email already exists.")
        return redirect("/register")

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/register")

    hashed_pw = bcrypt.hashpw(
        request.POST["password"].encode(), bcrypt.gensalt()
    ).decode()

    user1 = User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        password=hashed_pw,
    )
    request.session["log_user_id"] = user1.id
    return redirect("/home")


def home(request):
    context = {
        "user": User.objects.get(id=request.session["log_user_id"]),
        "reviews": Review.objects.order_by("-created_at")[:2],
        'retailers': Retailer.objects.order_by('-created_at')[:2]
    }
    return render(request, "home.html", context)


def logout(request):
    request.session.clear()
    return redirect("/")


def profile(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'reviews': Review.objects.filter(author=request.session['log_user_id']).order_by('-created_at')[:3]
    }
    return render(request, 'profile.html', context)

def edit_user(request, id):
    errors = User.objects.edit_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/profile')
    
    user = User.objects.get(id=id)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect('/profile')

def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('/')

def user(request, id):
    context = {
        'author': User.objects.get(id=id),
        'reviews': Review.objects.filter(author=id)
    }
    return render(request, 'user.html', context)

def reviews(request):
    context = {
        'reviews': Review.objects.all()
    }
    return render(request, 'reviews.html', context)

def retailer(request, id):
    context = {
        'retailer': Retailer.objects.get(id=id),
        'reviews': Review.objects.filter(retailer=id),
    }
    return render(request, 'retailer.html', context)

def add_retailer(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id'])
    }
    return render(request, 'add_retailer.html', context)

def create_retailer(request):
    errors = Retailer.objects.retailer_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/add_retailer')
    
    retailer1 = Retailer.objects.create(
        retailer = request.POST['retailer'],
        type = request.POST['type'],
        specialty = request.POST['specialty'],
        city = request.POST['city'],
        state = request.POST['state'],
    )

    return redirect(f'/retailer/{retailer1.id}')

def create_review1(request, id):
    errors = Review.objects.review_validator(request.POST)
    
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/retailer/{id}')

    review = Review.objects.create(
        review = request.POST['review'],
        retailer = Retailer.objects.get(id=id),
        author = User.objects.get(id=request.session['log_user_id'])
    )

    return redirect(f'/retailer/{id}')

def add_review(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'retailers': Retailer.objects.all()
    }
    return render(request, 'add_review.html', context)

def create_review2(request):
    errors = Review.objects.review_validator(request.POST)
    
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/add_review')

    review1 = Review.objects.create(
        review = request.POST['review'],
        retailer = Retailer.objects.get(id=request.POST['retailer']),
        author = User.objects.get(id=request.session['log_user_id'])
    )

    return redirect(f'/retailer/{review1.retailer.id}')

def reviews(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'reviews': Review.objects.all()
    }
    return render(request, 'reviews.html', context)

def retailers(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'retailers': Retailer.objects.all()
    }
    return render(request, 'retailers.html', context)

def like1(request, id):
    user = User.objects.get(id=request.session['log_user_id'])
    review = Review.objects.get(id=id)
    review.likes.add(user)
    return redirect('/home')

def like2(request, id):
    user = User.objects.get(id=request.session['log_user_id'])
    review = Review.objects.get(id=id)
    review.likes.add(user)
    return redirect('/reviews')

def like3(request, id):
    user = User.objects.get(id=request.session['log_user_id'])
    review = Review.objects.get(id=id)
    review.likes.add(user)
    return redirect(f'/retailer/{review.retailer.id}')

def like4(request, id):
    user = User.objects.get(id=request.session['log_user_id'])
    review = Review.objects.get(id=id)
    review.likes.add(user)
    return redirect(f'/user/{user.id}')

def edit_review(request, id):
    context = {
        'review': Review.objects.get(id=id)
    }
    return render(request, 'edit_review.html', context)

def update_review(request, id):
    errors = Review.objects.review_validator(request.POST)
    
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/edit_review')

    review = Review.objects.get(id=id)
    review.review = request.POST['review']
    return redirect('/profile')

def delete_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('/profile')

# Create your views here.
