from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('add-client/', views.add_client, name='add-client'),
    path('client/<int:client_id>', views.view_client, name='client'),
    path('clients/', views.view_clients, name='clients'),
    path('edit-client/<int:client_id>', views.edit_client, name='edit-client'),
    path('delete-client/<int:client_id>', views.delete_client, name='delete-client'),

    path('add-course/', views.add_course, name='add-course'),
    path('course/<int:course_id>', views.view_course, name='course'),
    path('courses/', views.view_courses, name='courses'),
    path('edit-course/<int:course_id>', views.edit_course, name='edit-course'),
    path('delete-course/<int:course_id>', views.delete_course, name='delete-course'),

    path('course/<int:course_id>/add-student', views.add_student, name='add-student'),
    path('delete-student/<int:course_id>/<int:student_id>', views.delete_student, name='delete-student'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
