from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def home(request):
    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    # when we want to submit data use POST method and when we want to fetch data use GET method
    messages.success(request, 'Welcome to the iCoder.')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 11 or len(content) < 4:
            messages.error(request, "please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been sent successfully")

    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        # allPosts = Post.objects.all()
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostContent)

    if allPosts.count() == 0:
        messages.warning(request, "please search  correctly")

    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

# Authentication APIs
def handleSignup(request):
    # Get the post parameters
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # check for errornous inputs
        # user name must be 10 character
        if len(username) > 10:
            messages.error(request, "username must be under 10 characher")
            return redirect('home')
        # username should be alphanumeric
        if not username.isalnum():
            messages.error(request, "username should contain letters and number")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect('home')

        # create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your iCoder  account has been successfully created')
        return redirect("home")


    else:
        return HttpResponse('404 - Not Found ')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername,
                            password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "successfully")
            return redirect('home')
        else:
            messages.error(request, 'Invalid  Credentials please try again ')
            return redirect('home')

    return HttpResponse('404 - not found')


def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully Logout')

    return redirect('home')



