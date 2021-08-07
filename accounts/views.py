from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from . import forms


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
