from django.urls import path
from .views import logoutview, CommentListview, CommentCreateView, CreateUser, CustomLoginView, UserCreateDone, UserCreateComplete

app_name  = 'fudaichat'

urlpatterns = [
    # path('signup/', signupview, name='signup'),
    path('', CreateUser.as_view(), name='user_create'),
    path('signup/done', UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', UserCreateComplete.as_view(), name='user_create_complete'),
    # path('login/', loginview, name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('list/', CommentListview.as_view(), name='list'),
    path('create/', CommentCreateView.as_view(), name='comment_create'),
    path('logout/', logoutview, name='logout'),
]
