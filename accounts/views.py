from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from .models import UserActivateTokens


def home(request):
    return render(
        request, 'accounts/home.html'
    )


def register(request):
    register_form = forms.RegisterForm(request.POST or None)

    if register_form.is_valid():
        try:
            # RegisterFormでオーバーライドしたsaveメソッドを呼び出す
            register_form.save()
            # ホーム画面にリダイレクト
            return redirect('accounts:home')
        except ValidationError as e:
            register_form.add_error('password', e)

    return render(
        request,
        'accounts/register.html',
        context={
            'register_form': register_form
        }
    )


def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'ログイン完了しました。')
                return redirect('accounts:home')
            else:
                messages.warning(request, 'ユーザがアクティブではありません。')
        else:
            messages.warning(request, 'ユーザかパスワードが間違っています。')

    return render(
        request,
        'accounts/login.html',
        context={
            'login_form': login_form,
        }
    )


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('accounts:home')


# activate_user: ユーザをアクティブにする
def activate_user(request, token):
    UserActivateTokens.objects.activate_user_by_token(token)
    return render(
        request,
        'accounts/activate_user.html'
    )

