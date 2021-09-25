from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Question, Response
from django import forms

User = get_user_model()

# UserCreationフォームではpassword1とpassword2が単純なフィールドとして定義されていることに注意です。つまり、Meta内でwidget=...といった上書きはできないことを意味します。なので、forms.pyにてこれらのcssのclassをいじりたい場合は__init__メソッドやクラスのフィールドとして定義しなおす必要があります。

class CustomUserCreateForm(UserCreationForm):
    # https://www.nblog09.com/w/2019/05/01/django-modelform/
    class Meta:
        model = User
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': True,
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@edu.osakafu-u.ac.jp'
            }),
        }

    #clean_email()メソッドは同じメールアドレスで仮登録段階のアカウントを消去しています
    def clean_email(self):
        email = self.cleaned_data['email']
        if "@edu.osakafu-u.ac.jp" not in email:   # any check you need
            raise forms.ValidationError("登録に使えるのはedu.osakafu-u.ac.jpを持つメールアドレスのみです。")
        User.objects.filter(email=email, is_active=False).delete()
        return email


class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


# 変更

class NewQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': True,
                'placeholder': '質問タイトルを入力してください。'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '回答内容を入力してください。'
            })
        }

class NewResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': '回答内容を入力してください。'
            })
        }

class NewReplyForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '返信内容を入力してください。'
            })
        }