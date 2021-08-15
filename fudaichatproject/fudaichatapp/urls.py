from django.urls import path
from .views import TopPage, QuestionListview, CreateUser, UserCreateDone, UserCreateComplete, ProfileView, DeleteUserComfirmView, DeleteUserCompleteView, questionPage, replyPage, newQuestionPage

app_name  = 'fudaichat'

urlpatterns = [
    path('', TopPage.as_view(), name='top_page'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('signup/done', UserCreateDone.as_view(), name='signup_done'),
    path('signup/complete/<token>/', UserCreateComplete.as_view(), name='signup_complete'),
    path('list/', QuestionListview.as_view(), name='list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete_confirm', DeleteUserComfirmView.as_view(template_name='registration/delete_confirm.html'), name='delete_confirm'),
    path('delete_complete', DeleteUserCompleteView.as_view(), name='delete_complete'),
    path('new_question', newQuestionPage, name='new_question'),
    path('question/<int:id>/', questionPage, name='question'),
    path('reply', replyPage, name='reply')
]
