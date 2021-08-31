from django.urls import path
from .views import TopPage, QuestionListView, CreateUser, UserCreateDone, UserCreateComplete,\
ProfileView, DeleteUserComfirmView, DeleteUserCompleteView, questionPage, replyPage, newQuestionPage,\
likeview, LikedQuestionListView, my_question_list

app_name  = 'fudaichat'

urlpatterns = [
    path('', TopPage.as_view(), name='top_page'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('signup/done', UserCreateDone.as_view(), name='signup_done'),
    path('signup/complete/<token>/', UserCreateComplete.as_view(), name='signup_complete'),
    path('list/', QuestionListView.as_view(), name='list'),
    path('liked_list/', LikedQuestionListView.as_view(),name='liked_list'),
    path('my_q_list', my_question_list, name='my_q_list'),
    path('like/', likeview, name='like'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete_confirm', DeleteUserComfirmView.as_view(template_name='registration/delete_confirm.html'), name='delete_confirm'),
    path('delete_complete', DeleteUserCompleteView.as_view(), name='delete_complete'),
    path('new_question', newQuestionPage, name='new_question'),
    path('question/<int:id>/', questionPage, name='question'),
    path('reply', replyPage, name='reply')
]
