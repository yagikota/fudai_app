from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView, CreateView, TemplateView, View
from .models import Question, Response, Likes
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreateForm, NewQuestionForm, NewReplyForm, NewResponseForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import dumps
from django.template.loader import render_to_string
from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired, loads
from django.contrib.auth import get_user_model
from pure_pagination.mixins import PaginationMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
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
        user.is_active = False
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


class QuestionListView(PaginationMixin, ListView):
    template_name = 'list.html'
    model = Question
    context_object_name = 'questions'
    paginate_by = 1

    def get_queryset(self):
        sort_order = self.request.GET.get('sort_order')
        if sort_order == 'date_desc':
            return Question.objects.order_by('-created_at')
        elif sort_order == 'date_asc':
            return Question.objects.order_by('created_at')
        elif sort_order == 'ans_desc':
            return Question.objects.annotate(num_responses=Count('responses')).order_by('-num_responses')
        elif sort_order == 'ans_asc':
            return Question.objects.annotate(num_responses=Count('responses')).order_by('num_responses')
        else:
            return Question.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.all()
        liked_list = []
        for question in questions:
            liked = question.likes.filter(author=self.request.user)
            if liked.exists():
                liked_list.append(question.id)
        context['liked_list'] = liked_list
        return context


def likeview(request):
    if request.method =="POST":
        question = get_object_or_404(Question, pk=request.POST.get('question_id'))
        author = request.user
        liked = False
        like = Likes.objects.filter(question=question, author=author)
        if like.exists():
            like.delete()
        else:
            like.create(question=question, author=author)
            liked = True

        context={
            'question_id': question.id,
            'liked': liked,
            'count': question.likes.count(),
        }

    if request.is_ajax():
        return JsonResponse(context)

class LikedQuestionListView(PaginationMixin, ListView):
    template_name = 'registration/liked_question_list.html'
    context_object_name = 'liked_questions'
    paginate_by = 1

    # 自分がいいねした質問のquerysetを取得
    def get_queryset(self):
        id_list = [likes.question.id for likes in Likes.objects.filter(author=self.request.user)]
        question =  Question.objects.filter(id__in=id_list)
        sort_order = self.request.GET.get('sort_order')
        if sort_order == 'date_desc':
            return question.order_by('-created_at')
        elif sort_order == 'date_asc':
            return question.order_by('created_at')
        elif sort_order == 'ans_desc':
            return question.annotate(num_responses=Count('responses')).order_by('-num_responses')
        elif sort_order == 'ans_asc':
            return question.annotate(num_responses=Count('responses')).order_by('num_responses')
        else:
            return question.annotate(num_likes=Count('likes')).order_by('-num_likes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.all()
        liked_list = []
        for question in questions:
            liked = question.likes.filter(author=self.request.user)
            if liked.exists():
                liked_list.append(question.id)
        context['liked_list'] = liked_list
        return context

class MyQuestionListView(PaginationMixin, ListView):
    template_name = 'registration/my_question_list.html'
    context_object_name = 'my_questions'
    paginate_by = 1

    # 自分がした質問のquerysetを取得
    def get_queryset(self):
        question =  Question.objects.filter(author=self.request.user)
        sort_order = self.request.GET.get('sort_order')
        if sort_order == 'date_desc':
            return question.order_by('-created_at')
        elif sort_order == 'date_asc':
            return question.order_by('created_at')
        elif sort_order == 'ans_desc':
            return question.annotate(num_responses=Count('responses')).order_by('-num_responses')
        elif sort_order == 'ans_asc':
            return question.annotate(num_responses=Count('responses')).order_by('num_responses')
        else:
            return question.annotate(num_likes=Count('likes')).order_by('-num_likes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_questions = Question.objects.filter(author=self.request.user)
        liked_list = []
        for question in my_questions:
            liked = question.likes.filter(author=self.request.user)
            if liked.exists():
                liked_list.append(question.id)
        context['liked_list'] = liked_list
        return context


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


# 変更

def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'comment_create.html', context)

def questionPage(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.author = request.user
                response.question = Question(id=id)
                response.save()
                return redirect('/question/'+str(id)+'#'+str(response.id))
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(id=id)
    context = {
        'question': question,
        'response_form': response_form,
        'reply_form': reply_form,
    }
    return render(request, 'question.html', context)


def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.author = request.user
                reply.question = Question(id=question_id)
                reply.parent = Response(id=parent_id)
                reply.save()
                return redirect('/question/'+str(question_id)+'#'+str(reply.id))
        except Exception as e:
            print(e)
            raise

    return redirect('list')