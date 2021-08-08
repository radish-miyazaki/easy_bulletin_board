from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import forms
from .models import Themes, Comments


def create_theme(request):
    create_theme_form = forms.CreateThemeForm(request.POST or None)
    if create_theme_form.is_valid():
        # ログイン中のユーザを設定
        create_theme_form.instance.user = request.user

        create_theme_form.save()
        messages.success(request, '掲示板を作成しました。')
        return redirect('boards:list_themes')

    return render(request, 'boards/create_theme.html', context={
        'create_theme_form': create_theme_form,
    })


def list_themes(request):
    themes = Themes.objects.fetch_all_themes()
    return render(
        request,
        'boards/list_themes.html',
        context={
            'themes': themes,
        }
    )


def edit_theme(request, id):
    theme = get_object_or_404(Themes, id=id)

    # 作成者とログインユーザが異なる場合は404エラーを起こす
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.EditThemeForm(request.POST or None, instance=theme)

    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request, '掲示板を更新しました')
        return redirect('boards:list_themes')

    return render(
        request,
        'boards/edit_theme.html',
        context={
            'edit_theme_form': edit_theme_form,
            'id': id,
        }
    )


def delete_theme(request, id):
    theme = get_object_or_404(Themes, id=id)

    if theme.user.id != request.user.id:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)

    if delete_theme_form.is_valid():  # csrf_token check
        theme.delete()
        messages.success(request, '掲示板を削除しました')
        return redirect('boards:list_themes')

    return render(
        request,
        'boards/delete_theme.html',
        context={
            'delete_theme_form': delete_theme_form,
        }
    )


def post_comments(request, theme_id):
    post_comment_form = forms.PostCommentForm(request.POST or None)
    theme = get_object_or_404(Themes, id=theme_id)
    comments = Comments.objects.fetch_by_theme_id(theme_id)

    if post_comment_form.is_valid():
        # Commentsインスタンスのthemeフィールドにquery_param(theme_id)から取得したThemeインスタンスをセット
        post_comment_form.instance.theme = theme
        # 同様にログインユーザをセット
        post_comment_form.instance.user = request.user
        post_comment_form.save()

        messages.success(request, 'コメントに成功しました')
        return redirect('boards:post_comments', theme_id=theme_id)

    return render(
        request,
        'boards/post_comments.html',
        context={
            'post_comment_form': post_comment_form,
            'theme': theme,
            'comments': comments,
        }
    )
