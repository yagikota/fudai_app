from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView, TemplateView
from .models import Comment
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CustomUserCreateForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import dumps
from django.template.loader import get_template, render_to_string
from .forms import CustomLoginForm, MyPasswordChangeForm, MySetPasswordForm, MyPasswordResetForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired, loads
from django.contrib.auth import get_user_model


# Create your views here.
User = get_user_model()

class TopPage(TemplateView):
    template_name = 'top_page.html'


# login
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('fudaichat:list')
        return super().get(request, **kwargs)


# sign up
class CreateUser(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreateForm
    # success_url = reverse_lazy('signup_done')

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().get(request, **kwargs)

    def form_valid(self, form):

        # 仮登録
        user = form.save(commit=False)# formの情報を保存
        user.is_active = False#is_active=Falseにすることで仮登録にする
        user.save()

        # メール送信
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            #django.core.signing.dumpを使うことで、tokenを生成しています。これはsettings.pyのSECRET_KEYの値等から生成される文字列で、第三者が推測しずらい文字列です。この文字列をもとに、本登録用のURLを作成し、そのURLをメールで伝えるという流れです。
            'token': dumps(user.pk),
            'user': user
        }
        # subject_template = get_template('mail/subject.txt')
        # message_template = get_template('mail/message.txt')
        # subject = subject_template.render(context)
        # message = message_template.render(context)
        subject = render_to_string('mail/subject.txt', context)
        message = render_to_string('mail/message.txt', context)
        user.email_user(subject, message)
        return redirect('fudaichat:signup_done')


class UserCreateDone(TemplateView):
    # 仮登録完了
    template_name = 'signup_done.html'

    # 必要？
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().get(request, **kwargs)


class UserCreateComplete(TemplateView):
    # 本登録完了
    template_name = 'signup_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        # tokenが正しければ本登録.
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        token = kwargs.get('token')
        try:
            #django.core.signing.dumps(user.pk)として作成したトークンは、django.core.signing.loads(token)としてuserのpkに復号化できます。 max_ageで有効期限の設定が可能です。
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return HttpResponseBadRequest()

        if not user.is_active:
            # 問題なければ本登録とする
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, **kwargs)

        return HttpResponseBadRequest()



class CommentListview(ListView):
    template_name = 'list.html'
    model = Comment
    queryset = Comment.objects.order_by('-post_date')
    context_object_name = 'comment_all_items'
    paginate_by = 10


class CommentCreateView(CreateView):
    template_name = 'comment_create.html'
    model = Comment
    fields = ('content',)
    context_object_name = 'comment_all_items'
    success_url = reverse_lazy('fudaichat:list')


    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        self.object = comment = form.save()
        messages.success(self.request, 'コメントを投稿しました')
        return super().form_valid(form)

class ProfileView(TemplateView):
    template_name = 'registration/profile.html'


class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('registration/password_change_done')
    template_name = 'registration/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'register/password_change_done.html'


class PasswordReset(PasswordResetView):
    # """パスワード変更用URLの送付ページ"""
    subject_template_name = 'fudaichat/mail_template/password_reset/subject.txt'
    email_template_name = 'fudaichat/mail_template/password_reset/message.txt'
    template_name = 'fudaichat/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('fudaichat:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    # """パスワード変更用URLを送りましたページ"""
    template_name = 'fudaichat/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    # """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('fudaichat:password_reset_complete')
    template_name = 'fudaichat/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    # """新パスワード設定しましたページ"""
    template_name = 'fudaichat/password_reset_complete.html'


def logoutview(request):
    logout(request)
    return redirect('fudaichat:top_page')
