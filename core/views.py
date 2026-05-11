from urllib.parse import quote

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import LoginForm, ProfileForm, SignUpForm


def _safe_next_url(request, value, fallback):
    if value and url_has_allowed_host_and_scheme(value, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return value
    return fallback


def login_view(request):
    if request.user.is_authenticated:
        return redirect(_safe_next_url(request, request.GET.get('next'), 'index'))
    next_url = request.POST.get('next') or request.GET.get('next')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        auth_login(request, form.user)
        return redirect(_safe_next_url(request, next_url, 'index'))
    return render(request, 'core/login.html', {'form': form, 'next_url': next_url or ''})


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        auth_login(request, user)
        return redirect('index')
    return render(request, 'core/signup.html', {'form': form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'core/profile.html', {'form': form})


@require_POST
def logout_view(request):
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    auth_logout(request)
    return redirect(_safe_next_url(request, next_url, 'index'))
