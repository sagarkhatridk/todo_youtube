from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from .forms import TodoForm
from .models import TODO
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TodoForm()
        todos = TODO.objects.filter(user=user).order_by('priority')
        context = dict(form=form, todos=todos)
        return render(request, 'index.html', context)


def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        param = {'loginform': form}
        return render(request, 'login.html', param)
    else:
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            param = {'loginform': form}
            return render(request, 'login.html', param)


def signout(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
        params = {'form': form}
        return render(request, 'signup.html', params)
    else:
        form = UserCreationForm(request.POST)
        params = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'signup.html', params)


@login_required(login_url='login')
def addtodo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TodoForm(request.POST)

        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect('home')
        else:
            context = dict(form=form)
            return render(request, 'index.html', context)


@login_required(login_url='login')
def delete_todo(request, pk):
    TODO.objects.get(pk=pk).delete()
    return redirect('home')


def updatetodo(request, pk, status):

    todo = TODO.objects.get(pk=pk)
    todo.status = status
    todo.save()
    return redirect('home')
