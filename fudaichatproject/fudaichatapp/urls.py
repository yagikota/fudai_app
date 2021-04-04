from django.urls import path
from .views import TopPage, logoutview, CommentListview, CommentCreateView, CreateUser, CustomLoginView, UserCreateDone, UserCreateComplete

app_name  = 'fudaichat'

urlpatterns = [
    path('', TopPage.as_view(), name='top_page'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('signup/done', UserCreateDone.as_view(), name='signup_done'),
    path('signup/complete/<token>/', UserCreateComplete.as_view(), name='signup_complete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('list/', CommentListview.as_view(), name='list'),
    path('create/', CommentCreateView.as_view(), name='comment_create'),
    path('logout/', logoutview, name='logout'),
]
