from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Users


class RegisterForm(forms.ModelForm):
    # Form fields
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput)

    # Meta data
    class Meta:
        model = Users
        fields = ('username', 'age', 'email', 'password')

    # Validations
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません。')

    def save(self, commit=False):
        user = super().save(commit=False)
        # パスワードが正しいかどうか
        validate_password(self.cleaned_data.get('password'), user)

        # Hash化したパスワードをセット
        user.set_password(self.cleaned_data.get('password'))

        user.save()
        return user
