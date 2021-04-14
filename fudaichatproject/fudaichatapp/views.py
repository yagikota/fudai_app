from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView, CreateView, TemplateView, View
from .models import Comment
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CustomUserCreateForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import dumps
from django.template.loader import render_to_string
from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired, loads
from django.contrib.auth import get_user_model


# Create your views here.
User = get_user_model()

class TopPage(TemplateView):
    template_name = 'top_page.html'


class CreateUser(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreateForm

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().get(request, **kwargs)

    def form_valid(self, form):

        # 仮登録
        user = form.save(commit=False)
        user.is_active = False#
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user
        }

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


class DeleteUserComfirmView(TemplateView):
    template_name = 'registration/delete_confirm.html'


class DeleteUserCompleteView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        # 大元のデータベースから削除
        User.objects.filter(email=self.request.user.email).delete()
        auth_logout(self.request)
        return render(self.request,'top_page.html')