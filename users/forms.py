from django_registration.forms import RegistrationForm
from users.models import CustomUser
from django import forms



class CustomUserForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = CustomUser


    def clean_username(self):

        username = self.cleaned_data.get("username")

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already exists")
        
        return username

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not any(char.isalpha() for char in password) or not password.isascii():
            
            raise forms.ValidationError("The password must contain only Latin characters")
        
        return password
        

    

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch")
        
        return password2
