from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Client


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Электронная почта'}))
    first_name = forms.CharField(label="", required=True, max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Фамилия'}))
    middle_name = forms.CharField(label="", required=True, max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label="", required=False, max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Отчество'}))
    username = forms.CharField(label="", required=True, max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Имя пользователя'}), help_text=(
        '<span class="form-text text-muted"><small>Обязательно. Не больше 50 символов.'
        ' Только буквы, цифры и символы @/./+/-/_ .</small></span>'))
    password1 = forms.CharField(
        label="", required=True, min_length=8, max_length=100, widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Пароль'}), help_text=(
            '<ul class="form-text text-muted small"><li>Пароль не должен быть схожим с'
            ' персональными данными.</li><li>Пароль должен содержать как минимум '
            '8 символов.</li><li>Пароль не должен быть слишком простым.'
            '</li><li>Пароль не должен состоять только из цифр.</li></ul>'))
    password2 = forms.CharField(label="", required=True, max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Подтверждение пароля'}), help_text=(
        '<span class="form-text text-muted"><small>Введите пароль еще раз для верификации.</small></span>'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'email', 'password1', 'password2')

    def __int__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)


class AddClientForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={
        "placeholder": "Фамилия", "class": "form-control"}), label="")
    middle_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={
        "placeholder": "Имя", "class": "form-control"}), label="")
    last_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={
        "placeholder": "Отчество", "class": "form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={
        "placeholder": "e-mail", "class": "form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={
        "placeholder": "Мобильный телефон", "class": "form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={
        "placeholder": "Адрес", "class": "form-control"}), label="")
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={
        "placeholder": "Город", "class": "form-control"}), label="")
    state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={
        "placeholder": "Область", "class": "form-control"}), label="")

    class Meta:
        model = Client
        exclude = ("user",)
