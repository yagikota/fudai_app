from django.http import request
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
from .forms import CustomLoginForm
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired, loads
from . import utils


# Create your views here.

class CreateUser(CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('user_crate_done')

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().get(request, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります

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
        return redirect('fudaichat:user_create_done')


class UserCreateDone(TemplateView):
    # 仮登録完了
    template_name = 'user_create_done.html'

    # 必要？
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().get(request, **kwargs)


class UserCreateComplete(TemplateView):
    # 本登録完了
    template_name = 'user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        # tokenが正しければ本登録.
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        token = kwargs.get('token')
        # try:
            #django.core.signing.dumps(user.pk)として作成したトークンは、django.core.signing.loads(token)としてuserのpkに復号化できます。 max_ageで有効期限の設定が可能です。
        user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        # except SignatureExpired:
        #     return HttpResponseBadRequest()

        # # tokenが間違っている
        # except BadSignature:
        #     return HttpResponseBadRequest()

        # tokenは問題なし
        # try:
        user = User.objects.get(pk=user_pk)
        # except User.DoesNotExist:
            # return HttpResponseBadRequest()

        if not user.is_active:
            # 問題なければ本登録とする
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # QRコード生成
            # request.session["img"] = utils.get_image_b64(utils.get_auth_url(user.email, utils.get_secret(user)))

            return super().get(request, **kwargs)

        return render(request, 'usr_create_complete_html', {})



class CustomLoginView(LoginView):
    # ログイン
    form_class = CustomLoginForm
    template_name = 'login.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('fudaichat:list')
        return super().get(request, **kwargs)


# def signupview(request):
#     if request.method == 'POST':
#         username_data = request.POST['username_data']
#         mailaddress_data = request.POST['mailaddress_data']
#         password_data = request.POST['password_data']
#         try:
#             User.objects.create_user(username_data, mailaddress_data + '@edu.osakafu-u.ac.jp', password_data)
#             # user.save()
#         except:
#             # return render(request, 'signup.html', {'error': 'このユーザーはすでに登録されています'})
#             return redirect('login')
#     else:
#         return render(request, 'signup.html', {})
#     return redirect('login')



# def loginview(request):
#     if request.method == 'POST':
#         username_data = request.POST['username_data']
#         password_data = request.POST['password_data']
#         user = authenticate(request, username=username_data, password=password_data)
#         if user is not None:
#             login(request, user)
#             return redirect('list')
#         else:
#             # Return an 'invalid login' error message.
#             return redirect('login')
#     return render(request, 'login.html')




class CommentListview(ListView):
    template_name = 'list.html'
    model = Comment
    queryset = Comment.objects.order_by('-post_date')
    context_object_name = 'comment_all_items'
    paginate_by = 5


class CommentCreateView(CreateView):
    template_name = 'comment_create.html'
    model = Comment
    queryset = Comment.objects.order_by('post_date')
    fields = ('content',)
    context_object_name = 'comment_all_items'
    success_url = reverse_lazy('fudaichat:list')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        self.object = comment = form.save()
        messages.success(self.request, 'コメントを投稿しました')
        return super().form_valid(form)


# https://qiita.com/godan09/items/97ea3a6397bf619b6517

def logoutview(request):
    logout(request)
    return redirect('fudaichat:login')
