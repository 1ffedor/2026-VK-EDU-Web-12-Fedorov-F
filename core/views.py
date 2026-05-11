from django.shortcuts import render


def login_view(request):
    return render(
        request,
        'core/login.html',
        {'show_login_error': True},
    )


def signup(request):
    return render(request, 'core/signup.html')


def profile(request):
    profile = getattr(request.user, 'profile', None) if request.user.is_authenticated else None
    email = request.user.email if request.user.is_authenticated else 'fedor@mail.ru'
    login = request.user.username if request.user.is_authenticated else 'fedor_dev'
    nickname = profile.nickname if profile and profile.nickname else 'Федор'
    return render(
        request,
        'core/profile.html',
        {
            'profile_stub': {
                'login': login,
                'email': email,
                'nickname': nickname,
            },
        },
    )
