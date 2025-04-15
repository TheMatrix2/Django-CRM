from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views
from . import views

router = DefaultRouter()
router.register(r'clients', api_views.ClientViewSet)
router.register(r'courses', api_views.CourseViewSet)

# API URL patterns
api_urlpatterns = [
    path('', include(router.urls)),
    path('login/', api_views.LoginView.as_view(), name='api_login'),
    path('logout/', api_views.logout_view, name='api_logout'),
    path('register/', api_views.RegisterView.as_view(), name='api_register'),
    path('profile/', api_views.profile_view, name='api_profile'),
]


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    # Client URLs
    path('clients/', views.view_clients, name='clients'),
    path('add-client/', views.add_client, name='add-client'),
    path('client/<int:client_id>', views.view_client, name='client'),
    path('edit-client/<int:client_id>', views.edit_client, name='edit-client'),
    path('delete-client/<int:client_id>', views.delete_client, name='delete-client'),

    # Course URLs
    path('courses/', views.view_courses, name='courses'),
    path('add-course/', views.add_course, name='add-course'),
    path('course/<int:course_id>', views.view_course, name='course'),
    path('edit-course/<int:course_id>', views.edit_course, name='edit-course'),
    path('delete-course/<int:course_id>', views.delete_course, name='delete-course'),
    path('add-student/<int:course_id>', views.add_student, name='add-student'),
    path('delete-student/<int:course_id>/<int:student_id>', views.delete_student, name='delete-student'),

    # Include the API URLs under 'api/' prefix
    path('api/', include(api_urlpatterns)),
    path('', include(router.urls)),
]