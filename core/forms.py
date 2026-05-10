from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Profile

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['username'].widget.attrs.update({'class': 'form-control rounded-pill', 'autocomplete': 'username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control rounded-pill', 'autocomplete': 'current-password'})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if not self.user:
                raise forms.ValidationError('Неверный логин или пароль')
        return cleaned_data


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', max_length=150)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')
        labels = {
            'username': 'Логин',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control rounded-pill', 'autocomplete': 'username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control rounded-pill', 'autocomplete': 'email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control rounded-pill', 'autocomplete': 'given-name'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control rounded-pill', 'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control rounded-pill', 'autocomplete': 'new-password'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают')
        return cleaned_data

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                cleaned_messages = []
                for msg in e.messages:
                    cleaned = msg.replace('Введённый пароль ', '').replace('Введенный пароль ', '')
                    if cleaned:
                        cleaned = cleaned[0].upper() + cleaned[1:]
                    cleaned_messages.append(cleaned)
                raise ValidationError(cleaned_messages)
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    username = forms.CharField(label='Логин', max_length=150)
    email = forms.EmailField(label='Email')

    class Meta:
        model = Profile
        fields = ('nickname', 'avatar')
        labels = {
            'nickname': 'Никнейм',
            'avatar': 'Аватар',
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
        self.fields['username'].widget.attrs.update({'class': 'form-control rounded-pill'})
        self.fields['email'].widget.attrs.update({'class': 'form-control rounded-pill'})
        self.fields['nickname'].widget.attrs.update({'class': 'form-control rounded-pill'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control form-control-sm', 'accept': 'image/*'})

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        qs = User.objects.filter(username=username)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise ValidationError('Этот логин уже занят')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        qs = User.objects.filter(email__iexact=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise ValidationError('Этот email уже занят')
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save(update_fields=['username', 'email'])
            profile.save()
        return profile
