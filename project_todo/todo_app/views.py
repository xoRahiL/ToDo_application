from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import Todo


def index(request):
    if request.user.is_authenticated:
        todos = Todo.objects.filter(user=request.user)
        user = request.user
    else:
        todos = Todo.objects.none()
        user = User.objects.none()

    return render(request, 'index.html', {'td': todos, 'u': user})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()

        myuser = authenticate(username=username, password=password)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Successful")
            return redirect('index')
        else:
            messages.error(request, "Incorrect Credentials!")
            return redirect('login')

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        fname = request.POST['fname'].strip()
        lname = request.POST['lname'].strip()
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fname,
            last_name=lname
        )
        user.save()
        messages.success(request, "Registration Successful")
        return redirect('login')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect('index')


def create(request):
    # First checking if user is authenticated(logged In)
    try:
        u = request.user.id
        myuser = User.objects.get(id=u)
    except ObjectDoesNotExist:
        messages.error(request, 'Login Required!')
        return redirect('index')

    if request.method == 'POST':
        try:
            title = request.POST['title'].strip()  # strip() removes white spaces
            description = request.POST['desc'].strip()
            print("before todo")
            todo = Todo(
                user=myuser,
                title=title,
                description=description
            )
            todo.save()
            print("todo saved!")
            return redirect('index')

        except Exception as e:
            # Log the error and show a friendly error message
            print(f"Error creating todo: {e}")
            return render(request, 'index.html', {'error': str(e)})

    return render(request, 'index.html')


def update(request, tid):
    td = Todo.objects.get(id=tid)
    if request.method == 'POST':
        todo = request.POST['title'].strip()
        description = request.POST['desc'].strip()

        td.todo = todo
        td.description = description
        td.save()

        return redirect('index')

    return render(request, 'edit.html', {'td': td})


def delete(request, tid):
    td = Todo.objects.get(id=tid)
    td.delete()

    return redirect('index')
