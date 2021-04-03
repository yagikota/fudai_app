from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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





class CustomLoginForm(AuthenticationForm):
    # カスタムログインフォーム
    # token = forms.CharField(max_length=254, label="Google Authenticator OTP")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    # def confirm_login_allowed(self, user):
    #     # 二要素認証チェック
    #     if utils.get_token(user) != self.cleaned_data.get('token'):
    #         raise forms.ValidationError(
    #             "'Google Authenticator OTP' is invalid."
    #         )
    #     super().confirm_login_allowed(user)
