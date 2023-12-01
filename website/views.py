from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddClientForm
from .models import Client
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html', {})


def account(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы вошли в систему!")
            return redirect('account')
        else:
            messages.warning(request, "Возникла ошибка при входе. Попробуйте еще раз.")
            return redirect('account')
    else:
        return render(request, 'account.html', {})

def view_clients(request):
    # Check to see if logging in
    if request.user.is_authenticated:
        clients = Client.objects.all()
        return render(request, 'clients.html', {'clients': clients})
    else:
        messages.success(request, "Возникла ошибка при входе. Попробуйте еще раз.")
        return redirect('login')


def login_user(request):
    # Проверка на login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Аутентификация
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы вошли в систему!")
            return redirect('account')
        else:
            messages.error(request, "Возникла ошибка при входе. Попробуйте еще раз.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Успешная регистрация! Добро пожаловать!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def add_client(request):
    form = AddClientForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Запись создана.")
                return redirect('clients')
        return render(request, 'add-client.html', {'form': form})
    else:
        messages.warning(request, "Для создания записей авторизуйтесь в системе.")
        return redirect('login')


def view_client(request, id):
    if request.user.is_authenticated:
        client = Client.objects.get(id=id)
        return render(request, 'client.html', {'client': client})
    else:
        messages.warning(request, "Для просмотра информации авторизируйтесь в системе.")
        return redirect('login')


def edit_client(request, id):
    to_edit = Client.objects.get(id=id)
    form = AddClientForm(request.POST or None, instance=to_edit)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Информация успешно обновлена.")
                return redirect('clients')
        return render(request, 'edit-client.html', {'form': form, 'to_edit': to_edit})
    else:
        messages.warning(request, "Для изменения информации авторизуйтесь в системе.")
        return redirect('login')


def delete_client(request, id):
    if request.user.is_authenticated:
        to_delete = Client.objects.get(id=id)
        to_delete.delete()
        messages.success(request, "Информация о клиенте успешно удалена.")
        return redirect('account')
    else:
        messages.warning(request, "Для удаления записей авторизуйтесь в системе.")
        return redirect('login')
