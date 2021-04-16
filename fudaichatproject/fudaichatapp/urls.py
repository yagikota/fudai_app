from django.urls import path
from .views import TopPage, CommentListview, CommentCreateView, CreateUser, UserCreateDone, UserCreateComplete, ProfileView, DeleteUserComfirmView, DeleteUserCompleteView
from django.contrib.auth import views as auth_views

app_name  = 'fudaichat'

urlpatterns = [
    path('', TopPage.as_view(), name='top_page'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('signup/done', UserCreateDone.as_view(), name='signup_done'),
    path('signup/complete/<token>/', UserCreateComplete.as_view(), name='signup_complete'),
    path('list/', CommentListview.as_view(), name='list'),
    path('create/', CommentCreateView.as_view(), name='comment_create'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete_confirm', DeleteUserComfirmView.as_view(template_name='registration/delete_confirm.html'), name='delete_confirm'),
    path('delete_complete', DeleteUserCompleteView.as_view(), name='delete_complete'),
]
