from django.urls import path,include
from users.forms import CustomUserForm
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth import views as auth_views

app_name = "users"


urlpatterns = [
    path("auth/", include('django.contrib.auth.urls')),
    path("accounts/register/",RegistrationView.as_view(
            form_class=CustomUserForm,
            success_url="/shop/home/"),           
            name="django_registration_register"
        ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]