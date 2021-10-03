from django.urls import path
from .views import LandPage, TopPage, QuestionListView,\
ProfileView, DeleteUserComfirmView, DeleteUserCompleteView, questionPage, replyPage, newQuestionPage,\
likeview, LikedQuestionListView, MyQuestionListView

app_name  = 'fudaichat'

urlpatterns = [
    path('', LandPage.as_view(), name='land_page'),
    path('top_page/', TopPage.as_view(), name='top_page'),
    path('list/', QuestionListView.as_view(), name='list'),
    path('liked_list/', LikedQuestionListView.as_view(),name='liked_list'),
    path('my_q_list', MyQuestionListView.as_view(), name='my_q_list'),
    path('like/', likeview, name='like'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete_confirm', DeleteUserComfirmView.as_view(), name='delete_confirm'),
    path('delete_complete', DeleteUserCompleteView.as_view(), name='delete_complete'),
    path('new_question', newQuestionPage, name='new_question'),
    path('question/<int:id>/', questionPage, name='question'),
    path('reply', replyPage, name='reply'), 
]
