from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import Client, Course


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html', {})


@login_required(login_url='/login')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


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
            return redirect('home')
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


@login_required(login_url='/login')
def add_client(request):
    form = AddClientForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Запись создана.")
            return redirect('clients')
    return render(request, 'clients/add-client.html', {'form': form})


@login_required(login_url='/login')
def view_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/clients.html', {'clients': clients})


@login_required(login_url='/login')
def view_client(request, client_id):
    client = Client.objects.get(id=client_id)
    course_titles = ['', '', '']
    if client.course_id_1 != 0:
        course_titles.append(Course.objects.get(id=client.course_id_1).title)
    if client.course_id_2 != 0:
        course_titles.append(Course.objects.get(id=client.course_id_2).title)
    if client.course_id_3 != 0:
        course_titles.append(Course.objects.get(id=client.course_id_3).title)
    previous_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'clients/client.html', {'client': client, 'courses': course_titles,
                                                   'previous_url': previous_url})


@login_required(login_url='/login')
def edit_client(request, client_id):
    to_edit = Client.objects.get(id=client_id)
    courses = Course.objects.all()
    form = AddClientForm(request.POST or None, instance=to_edit)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Информация успешно обновлена.")
            return render(request, 'clients/client.html', {'client': to_edit, 'courses': courses})
    return render(request, 'clients/edit-client.html', {'form': form, 'to_edit': to_edit,
                                                        'courses': courses})


@login_required(login_url='/login')
def delete_client(request, client_id):
    to_delete = Client.objects.get(id=client_id)
    if request.method == "POST":
        to_delete.delete()
        messages.success(request, "Информация о клиенте успешно удалена.")
        return redirect('clients')
    else:
        return render(request, 'clients/client.html', {'client': to_delete})


@login_required(login_url='/login')
def add_course(request):
    form = AddCourseForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Запись создана.")
            return redirect('courses')
    return render(request, 'courses/add-course.html', {'form': form})


@login_required(login_url='/login')
def view_courses(request):
    courses = Course.objects.all()
    return render(request, 'courses/courses.html', {"courses": courses})


@login_required(login_url='/login')
def view_course(request, course_id):
    course = Course.objects.get(id=course_id)
    students = (Client.objects.filter(course_id_1=course_id) | Client.objects.filter(course_id_2=course_id) |
                Client.objects.filter(course_id_3=course_id))
    course.number_of_students = len(students)
    course.save()
    return render(request, 'courses/course.html', {'course': course, 'students': students})


@login_required(login_url='/login')
def edit_course(request, course_id):
    to_edit = Course.objects.get(id=course_id)
    form = AddCourseForm(request.POST or None, instance=to_edit)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Информация успешно обновлена.")
            return redirect('course', course_id=to_edit.id)
    else:
        return render(request, 'courses/edit-course.html', {'form': form, 'to_edit': to_edit})


@login_required(login_url='/login')
def delete_course(request, course_id):
    to_delete = Course.objects.get(id=course_id)
    if request.method == "POST":
        to_delete.delete()
        messages.success(request, f'Курс "{to_delete.title}" удален')
        return redirect('courses')
    else:
        return render(request, 'courses/course.html', {'course': to_delete})


@login_required(login_url='/login')
def add_student(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        selected_student_ids = request.POST.getlist('selected_student_ids')
        ids_str = selected_student_ids[0]
        ids_str = ids_str.replace('[', '').replace(']', '').replace('"', '')
        ids = ids_str.split(',')
        for id in ids:
            new_student = Client.objects.get(id=int(id))
            student_courses = [new_student.course_id_1, new_student.course_id_2, new_student.course_id_3]
            if course.id in student_courses:
                messages.warning(request, f'{new_student.first_name} уже числится на этом курсе')
                continue
            if 0 in student_courses:
                student_courses[student_courses.index(0)] = course.id
                course.number_of_students += 1
                course.save()
                (new_student.course_id_1,
                 new_student.course_id_2, new_student.course_id_3) = (student_courses[0], student_courses[1],
                                                                      student_courses[2])
                new_student.save()
                messages.success(request, 'Клиент зачислен на курс')
            else:
                messages.warning(request, f'{str(new_student)} уже числится на максимально возможном '
                                          f'количестве курсов (3)')
        # return HttpResponse("Студенты успешно добавлены на курс.")
        return redirect('course', course_id=course.id)
    else:
        clients = (Client.objects.exclude(course_id_1=course.id) & Client.objects.exclude(course_id_2=course.id) &
                   Client.objects.exclude(course_id_3=course.id) & (Client.objects.filter(course_id_1=0) |
                                                                    Client.objects.filter(course_id_2=0) |
                                                                    Client.objects.filter(course_id_3=0)))
        return render(request, 'courses/add-student.html', {'clients': clients,
                                                            'course_id': course.id})


@login_required(login_url='/login')
def delete_student(request, course_id, student_id):
    course = Course.objects.get(id=course_id)
    student = Client.objects.get(id=student_id)
    student_courses = [student.course_id_1, student.course_id_2, student.course_id_3]
    if request.method == 'POST':
        if course_id in student_courses:
            course.number_of_students -= 1
            course.save()
            student_courses[student_courses.index(course.id)] = 0
            student.course_id_1, student.course_id_2, student.course_id_3 = (student_courses[0], student_courses[1],
                                                                             student_courses[2])
            student.save()
            messages.success(request, "Клиент больше не учится на этом курсе")
            return redirect('course', course_id=course_id)
        else:
            messages.warning(request, "На этом курсе нет такого клиента")
    return render(request, 'courses/course.html', {'course': course})

