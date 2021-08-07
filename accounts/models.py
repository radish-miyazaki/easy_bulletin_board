from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from datetime import datetime, timedelta
from django.contrib.auth.models import UserManager


"""
 Primary classes.
"""


class Users(AbstractBaseUser, PermissionsMixin):
    # Fields
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/')

    objects = UserManager()

    USERNAME_FIELD = 'email'  # 一意に識別フィールド
    REQUIRED_FIELDS = ['username']  # 作成時に必要なフィールド

    # Meta data
    class Meta:
        db_table = 'users'


class Comments(models):
    comment = models.TextField()
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE,
    )


class Themes(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE,
    )
    comments = models.ManyToManyField(Comments)


"""
 Classes to activate user.
"""


class UserActivateTokensManage(models.Manager):
    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        user = user_activate_token.user
        user.is_active = True
        user.save()


# ユーザをアクティブにするためのモデル
class UserActivateTokens(models.Model):
    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE,
    )
    # Managerを適用する
    objects = UserActivateTokensManage()

    class Meta:
        db_table = 'user_activate_tokens'


# モデルが新規追加されるたびに呼び出されるメソッド（シグナル）
@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    user_activate_token = UserActivateTokens.objects.create(
        user=instance,
        token=str(uuid4()),
        expired_at=datetime.now() + timedelta(days=1),
    )

    # FIXME: 本来はメールで送信する箇所。
    # FIXME: ここでは固定値で指定しているがenvに切り出す。
    print(f'http://localhost:3000/accounts/activate/{user_activate_token.token}')
