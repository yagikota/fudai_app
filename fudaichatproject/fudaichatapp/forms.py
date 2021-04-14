from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
# from django.db.models import fields
from . import utils
from django import forms

User = get_user_model()

# UserCreationフォームではpassword1とpassword2が単純なフィールドとして定義されていることに注意です。つまり、Meta内でwidget=...といった上書きはできないことを意味します。なので、forms.pyにてこれらのcssのclassをいじりたい場合は__init__メソッドやクラスのフィールドとして定義しなおす必要があります。

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        
    #clean_email()メソッドは同じメールアドレスで仮登録段階のアカウントを消去しています
    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


# class CustomLoginForm(AuthenticationForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['placeholder'] = field.label

# class MyPasswordChangeForm(PasswordChangeForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['placeholder'] = field.label

# class MyPasswordResetForm(PasswordResetForm):
#     # """パスワード忘れたときのフォーム"""

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'


# class MySetPasswordForm(SetPasswordForm):
#     # """パスワード再設定用フォーム(パスワード忘れて再設定)"""

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
