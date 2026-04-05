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
    return render(
        request,
        'core/profile.html',
        {
            'profile_stub': {
                'login': 'fedor_dev',
                'email': 'fedor@mail.ru',
                'nickname': 'Федор',
            },
        },
    )
